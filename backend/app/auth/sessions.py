import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any

from fastapi import Response
from pymongo.database import Database

from app.config import Settings
from app.db import Collections

SESSION_COOKIE = "jc_session"
SECONDS_PER_DAY = 86400


def _hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode()).hexdigest()


def create_session(
    db: Database[dict[str, Any]], user_id: str, *, ttl_days: int, now: datetime
) -> str:
    raw_token = secrets.token_urlsafe(32)
    db[Collections.SESSIONS].insert_one(
        {
            "_id": _hash_token(raw_token),
            "user_id": user_id,
            "created_at": now,
            "expires_at": now + timedelta(days=ttl_days),
        }
    )
    return raw_token


def resolve_session(
    db: Database[dict[str, Any]], raw_token: str, *, now: datetime
) -> str | None:
    session = db[Collections.SESSIONS].find_one({"_id": _hash_token(raw_token)})
    if session is None or session["expires_at"] <= now:
        return None
    return str(session["user_id"])


def revoke_session(db: Database[dict[str, Any]], raw_token: str) -> None:
    db[Collections.SESSIONS].delete_one({"_id": _hash_token(raw_token)})


def revoke_user_sessions(db: Database[dict[str, Any]], user_id: str) -> int:
    return db[Collections.SESSIONS].delete_many({"user_id": user_id}).deleted_count


def set_session_cookie(response: Response, token: str, settings: Settings) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        token,
        max_age=settings.session_ttl_days * SECONDS_PER_DAY,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        path="/",
    )


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE, path="/")
