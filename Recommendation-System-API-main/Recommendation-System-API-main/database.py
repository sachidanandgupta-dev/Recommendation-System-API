import sqlite3


def create_database():
    # Connect to a local SQLite database file named app.db.
    # If app.db does not exist yet, SQLite will create it automatically.
    connection = sqlite3.connect("app.db")

    # A cursor lets us run SQL commands on the database.
    cursor = connection.cursor()

    # Create a Users table to store basic user information.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Create a Content table to store items (like posts or resources).
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            content_type TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Create a Skills table to store skill names and optional levels.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL UNIQUE,
            skill_level TEXT
        )
        """
    )

    # Create an Interactions table to track user actions on content.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content_id INTEGER NOT NULL,
            interaction_type TEXT NOT NULL,
            interaction_time TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (content_id) REFERENCES Content(id)
        )
        """
    )

    # Save (commit) all table creation commands.
    connection.commit()

    # Close the database connection when done.
    connection.close()

    print("Database setup complete. app.db and tables are ready.")


# Run this file directly to create the database and tables.
if __name__ == "__main__":
    create_database()
