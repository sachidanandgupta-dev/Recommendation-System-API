<div align="center">

# Recommendation System API

**A production-style FastAPI backend with SQLite, cold-start handling, and history-aware recommendations.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

*RESTful JSON API · Automatic OpenAPI docs · Relational data model · Feedback loop for personalization*

</div>

---

## About the Project

This project is a **lightweight recommendation backend** built to demonstrate how modern APIs solve a classic problem: *what should we show a user when we know little about them, versus when we already have behavioral data?*

The service exposes a clean HTTP interface over a **SQLite** database with normalized tables for users, catalog content, and user–content **interactions**. On startup, the API seeds sample users and content so you can exercise the full flow immediately.

**Cold start** users—those with no prior interactions—receive a curated set of **trending** catalog items. Once a user submits **feedback** (ratings via a dedicated POST endpoint), the system switches to **smart recommendations**: items from the catalog that user has **not** yet interacted with, driving a simple but credible personalization loop suitable for portfolios and technical interviews.

---

## Features

| Capability | Description |
|------------|-------------|
| **Cold-start recommendations** | Detects users with zero interactions and returns a trending-style slice of the catalog. |
| **History-aware recommendations** | After feedback exists, recommends up to five unseen content items using SQL filtering. |
| **Feedback ingestion** | `POST /feedback` accepts validated JSON (`user_id`, `content_id`, `rating` 1–5) and persists to `Interactions`. |
| **User catalog** | `GET /users` lists registered users from the database for demos and debugging. |
| **Operational endpoints** | Health and metrics routes for monitoring-style checks and future observability. |
| **Auto-generated API docs** | FastAPI serves interactive OpenAPI/Swagger UI at `/docs`. |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python |
| **Web framework** | [FastAPI](https://fastapi.tiangolo.com/) — async-capable ASGI app, request validation, OpenAPI |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) — typed request bodies and field constraints |
| **Database** | [SQLite](https://www.sqlite.org/) — file-backed `app.db`, no separate server process |
| **DB access** | `sqlite3` (stdlib) — parameterized queries and `Row` factories for readable results |

---

## Repository Layout

```
Recommendation-System/
├── main.py          # FastAPI app, routes, recommendation & feedback logic
├── database.py      # One-time schema creation for Users, Content, Skills, Interactions
└── app.db           # SQLite file (created after running database.py / first API use)
```

---

## How to Run Locally

### Prerequisites

- **Python 3.10+** recommended  
- `pip` (bundled with most Python installs on Windows)

### 1. Clone and enter the project

```bash
cd Recommendation-System
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

### 4. Initialize the database (first time)

Creates `app.db` and tables if they do not exist:

```bash
python database.py
```

### 5. Start the API server

```bash
uvicorn main:app --reload
```

The API will be available at **http://127.0.0.1:8000**.

- **Interactive docs:** http://127.0.0.1:8000/docs  
- **Alternative docs:** http://127.0.0.1:8000/redoc  

On startup, `main.py` seeds dummy users and content (idempotent where applicable) so you can call `/recommendations/{user_id}` and `/feedback` without manual inserts.

---

## API Endpoints

Base URL (local): `http://127.0.0.1:8000`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness-style check; confirms the server process is responding. |
| `GET` | `/metrics` | Placeholder endpoint reserved for future observability metrics. |
| `GET` | `/users` | Returns all rows from the `Users` table as JSON. |
| `GET` | `/recommendations/{user_id}` | Returns recommendations for the given user: **cold start** (trending) if they have no interactions, otherwise **smart** recommendations (content not yet interacted with). Returns `User not found` if the ID is invalid. |
| `POST` | `/feedback` | JSON body: `user_id`, `content_id`, `rating` (1–5). Inserts into `Interactions` and returns success with `interaction_id`. Validates that user and content exist. |

### Example: submit feedback

```bash
curl -X POST "http://127.0.0.1:8000/feedback" ^
  -H "Content-Type: application/json" ^
  -d "{\"user_id\": 1, \"content_id\": 1, \"rating\": 5}"
```

*(On macOS/Linux, use `\` line continuation and single quotes for `-d` as preferred.)*

### Example: recommendations

```bash
curl "http://127.0.0.1:8000/recommendations/1"
```

---

## Why This Matters (for recruiters)

- **Problem framing:** Implements the distinction between **cold start** and **post-feedback** recommendation behavior—a core topic in recommender systems and product ML.  
- **Backend fundamentals:** REST design, request validation, relational modeling, and SQL that mirrors real filtering logic.  
- **Extensibility:** Clear separation between API layer and SQLite makes it straightforward to add collaborative filtering, embeddings, or a production database later.

---

## License

This project is provided as a portfolio / learning piece. Add a `LICENSE` file if you plan to open-source it formally.

---

<div align="center">

**Built with FastAPI · SQLite · Python**

</div>
