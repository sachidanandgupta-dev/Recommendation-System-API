This project is a lightweight recommendation backend built to demonstrate how modern APIs solve a classic problem: what should we show a user when we know little about them, versus when we already have behavioral data?

The service exposes a clean HTTP interface over a SQLite database with normalized tables for users, catalog content, and user–content interactions. On startup, the API seeds sample users and content so you can exercise the full flow immediately.

Cold start users—those with no prior interactions—receive a curated set of trending catalog items. Once a user submits feedback (ratings via a dedicated POST endpoint), the system switches to smart recommendations: items from the catalog that user has not yet interacted with, driving a simple but credible personalization loop suitable for portfolios and technical interviews.

Features
Capability	Description
Cold-start recommendations	Detects users with zero interactions and returns a trending-style slice of the catalog.
History-aware recommendations	After feedback exists, recommends up to five unseen content items using SQL filtering.
Feedback ingestion	POST /feedback accepts validated JSON (user_id, content_id, rating 1–5) and persists to Interactions.
User catalog	GET /users lists registered users from the database for demos and debugging.
Operational endpoints	Health and metrics routes for monitoring-style checks and future observability.
Auto-generated API docs	FastAPI serves interactive OpenAPI/Swagger UI at /docs.
Tech Stack
Layer	Technology
Language	Python
Web framework	FastAPI — async-capable ASGI app, request validation, OpenAPI
Validation	Pydantic — typed request bodies and field constraints
Database	SQLite — file-backed app.db, no separate server process
DB access	sqlite3 (stdlib) — parameterized queries and Row factories for readable results
Repository Layout
Recommendation-System/
├── main.py          # FastAPI app, routes, recommendation & feedback logic
├── database.py      # One-time schema creation for Users, Content, Skills, Interactions
└── app.db           # SQLite file (created after running database.py / first API use)
How to Run Locally
Prerequisites
Python 3.10+ recommended
pip (bundled with most Python installs on Windows)
1. Clone and enter the project
cd Recommendation-System
2. Create a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate
3. Install dependencies
pip install fastapi uvicorn pydantic
4. Initialize the database (first time)
Creates app.db and tables if they do not exist:

python database.py
5. Start the API server
uvicorn main:app --reload


