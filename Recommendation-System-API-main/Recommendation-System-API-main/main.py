import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Create a FastAPI app instance.
app = FastAPI(title="Recommendation System API")

# An endpoint is a URL path in your API (for example, /health).
# When a client sends a request to that path, your function runs
# and returns a response (usually JSON data).


class FeedbackRequest(BaseModel):
    # Data we expect in the POST /feedback JSON body.
    user_id: int
    content_id: int
    rating: int = Field(ge=1, le=5)


def get_db_connection():
    # Open a connection to app.db.
    connection = sqlite3.connect("app.db")

    # This lets us read columns by name (like row["email"]).
    connection.row_factory = sqlite3.Row
    return connection


def insert_dummy_users():
    # Add a couple of sample users so /users has data to return.
    # We use INSERT OR IGNORE so we do not insert duplicates
    # if the server restarts.
    connection = get_db_connection()
    cursor = connection.cursor()

    dummy_users = [
        ("alice", "alice@example.com"),
        ("bob", "bob@example.com"),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO Users (username, email)
        VALUES (?, ?)
        """,
        dummy_users,
    )

    connection.commit()
    connection.close()


def insert_dummy_content():
    # Add 5 sample content items so we have something to recommend.
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert only once to avoid duplicating the same items on restart.
    cursor.execute("SELECT COUNT(*) AS total FROM Content")
    total_items = cursor.fetchone()["total"]

    if total_items == 0:
        dummy_items = [
            ("Python Basics", "Learn variables, loops, and functions.", "course"),
            ("FastAPI Starter Guide", "Build your first API quickly.", "article"),
            ("SQL for Beginners", "Simple SQL queries with examples.", "course"),
            ("Backend Project Ideas", "Practice projects for new developers.", "article"),
            ("Debugging Tips", "How to find and fix common bugs.", "video"),
        ]

        cursor.executemany(
            """
            INSERT INTO Content (title, description, content_type)
            VALUES (?, ?, ?)
            """,
            dummy_items,
        )

    connection.commit()
    connection.close()


@app.on_event("startup")
def startup_event():
    # This function runs once when the FastAPI server starts.
    # We use it to seed initial dummy users and content.
    insert_dummy_users()
    insert_dummy_content()


@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()

    # First, make sure the user exists.
    cursor.execute("SELECT id, username FROM Users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        connection.close()
        return {"message": "User not found"}

    # How many times has this user given feedback? Drives Cold Start vs Smart path.
    cursor.execute(
        "SELECT COUNT(*) AS total FROM Interactions WHERE user_id = ?",
        (user_id,),
    )
    interaction_count = cursor.fetchone()["total"]

    if interaction_count == 0:
        # Cold Start: brand-new user — no history to learn from.
        # Show a fixed "trending" slice (same as before: newest items first).
        cursor.execute(
            """
            SELECT id, title, description, content_type
            FROM Content
            ORDER BY id DESC
            LIMIT 5
            """
        )
        message = "Cold Start: Here are the top 5 trending items"
    else:
        # Smart recommendations: user has history — suggest content they have not seen yet.
        # We pick rows from Content whose id is not in this user's interaction list.
        cursor.execute(
            """
            SELECT id, title, description, content_type
            FROM Content
            WHERE id NOT IN (
                SELECT content_id FROM Interactions WHERE user_id = ?
            )
            ORDER BY id
            LIMIT 5
            """,
            (user_id,),
        )
        message = "Smart Recommendations based on your history"

    items = cursor.fetchall()
    connection.close()

    recommended_items = []
    for item in items:
        recommended_items.append(
            {
                "id": item["id"],
                "title": item["title"],
                "description": item["description"],
                "content_type": item["content_type"],
            }
        )

    return {
        "message": message,
        "user_id": user_id,
        "items": recommended_items,
    }


@app.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    # Save user feedback into the Interactions table.
    connection = get_db_connection()
    cursor = connection.cursor()

    # Make sure user_id exists.
    cursor.execute("SELECT id FROM Users WHERE id = ?", (feedback.user_id,))
    user = cursor.fetchone()
    if user is None:
        connection.close()
        return {"message": "User not found"}

    # Make sure content_id exists.
    cursor.execute("SELECT id FROM Content WHERE id = ?", (feedback.content_id,))
    content = cursor.fetchone()
    if content is None:
        connection.close()
        return {"message": "Content not found"}

    # Our current Interactions table has an interaction_type text column.
    # We store the rating in that column as a simple string like "rating:5".
    interaction_type_value = f"rating:{feedback.rating}"

    cursor.execute(
        """
        INSERT INTO Interactions (user_id, content_id, interaction_type)
        VALUES (?, ?, ?)
        """,
        (feedback.user_id, feedback.content_id, interaction_type_value),
    )

    connection.commit()
    new_interaction_id = cursor.lastrowid
    connection.close()

    return {
        "message": "Feedback saved successfully",
        "interaction_id": new_interaction_id,
    }


@app.get("/health")
def health_check():
    # Health endpoint is used to confirm that the server is running.
    return {"message": "Health check passed"}


@app.get("/metrics")
def get_metrics():
    # Simple placeholder response for metrics.
    return {"message": "Metrics endpoint is working"}


@app.get("/users")
def get_users():
    # Fetch all users from the Users table and return them as JSON.
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, username, email, created_at
        FROM Users
        ORDER BY id
        """
    )
    rows = cursor.fetchall()
    connection.close()

    users = []
    for row in rows:
        users.append(
            {
                "id": row["id"],
                "username": row["username"],
                "email": row["email"],
                "created_at": row["created_at"],
            }
        )

    return {"users": users}
