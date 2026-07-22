import os
import sqlite3
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


DB_FILE = Path(os.getenv("SUBMISSIONS_DB", Path(__file__).with_name("submissions.db")))


class SubmissionIn(BaseModel):
    email: str
    training_code: str | None = None


class StatusIn(BaseModel):
    status: str


app = FastAPI(title="Day 3 Training API")
submission_attempts: dict[str, deque[datetime]] = defaultdict(deque)

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
    allow_methods=["GET", "POST", "PUT"],
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
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES ('status', 'live')"
        )


@app.on_event("startup")
def startup() -> None:
    init_db()


def get_status_value() -> str:
    init_db()
    with get_connection() as connection:
        row = connection.execute(
            "SELECT value FROM settings WHERE key = 'status'"
        ).fetchone()
    return row["value"] if row else "live"


def set_status_value(status: str) -> None:
    if status not in {"live", "stopped"}:
        raise HTTPException(status_code=400, detail="Status must be live or stopped")

    with get_connection() as connection:
        connection.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES ('status', ?)",
            (status,),
        )


def check_rate_limit(request: Request) -> None:
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=1)
    client_ip = request.client.host if request.client else "unknown"
    attempts = submission_attempts[client_ip]

    while attempts and attempts[0] < window_start:
        attempts.popleft()

    if len(attempts) >= 10:
        raise HTTPException(status_code=429, detail="Too many submissions")

    attempts.append(now)


@app.post("/api/submissions", status_code=201)
def create_submission(payload: SubmissionIn, request: Request) -> dict[str, str]:
    if get_status_value() == "stopped":
        raise HTTPException(status_code=409, detail="Form is currently stopped")

    check_rate_limit(request)
    email = payload.email.strip()

    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

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


@app.get("/api/status")
def get_status() -> dict[str, str]:
    return {"status": get_status_value()}


@app.put("/api/status")
def update_status(payload: StatusIn) -> dict[str, str]:
    set_status_value(payload.status)
    return {"status": payload.status}
