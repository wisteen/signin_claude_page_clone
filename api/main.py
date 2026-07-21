import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


DB_FILE = Path(os.getenv("SUBMISSIONS_DB", Path(__file__).with_name("submissions.db")))


class SubmissionIn(BaseModel):
    email: str
    password: str


app = FastAPI(title="Day 2 API")

origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                submitted_at TEXT NOT NULL
            )
            """
        )


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.post("/api/submissions", status_code=201)
def create_submission(payload: SubmissionIn) -> dict[str, str]:
    email = payload.email.strip()

    if not email or not payload.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    entry_id = str(uuid4())
    submitted_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute(
            "INSERT INTO submissions (id, email, submitted_at) VALUES (?, ?, ?)",
            (entry_id, email, submitted_at),
        )

    return {"status": "ok", "id": entry_id}


@app.get("/api/submissions")
def list_submissions() -> list[dict[str, str]]:
    init_db()
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, email, submitted_at FROM submissions ORDER BY submitted_at DESC"
        ).fetchall()

    return [dict(row) for row in rows]
