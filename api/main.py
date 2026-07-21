import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


DATA_FILE = Path(__file__).with_name("submissions.json")


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


def read_submissions() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        return []

    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail="Submission store is invalid") from exc


def write_submissions(submissions: list[dict[str, Any]]) -> None:
    DATA_FILE.write_text(
        json.dumps(submissions, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


@app.post("/api/submissions", status_code=201)
def create_submission(payload: SubmissionIn) -> dict[str, str]:
    email = payload.email.strip()

    if not email or not payload.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    submissions = read_submissions()
    entry = {
        "id": str(uuid4()),
        "email": email,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }
    submissions.append(entry)
    write_submissions(submissions)

    return {"status": "ok", "id": entry["id"]}


@app.get("/api/submissions")
def list_submissions() -> list[dict[str, Any]]:
    return read_submissions()
