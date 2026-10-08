from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import FastAPI, Response
from fastapi.testclient import TestClient
from pymongo.database import Database

from app.auth.sessions import (
    SESSION_COOKIE,
    clear_session_cookie,
    create_session,
    resolve_session,
    revoke_session,
    revoke_user_sessions,
    set_session_cookie,
)
from app.config import Settings

NOW = datetime(2026, 10, 8, 12, 0, tzinfo=UTC)


def test_token_is_stored_hashed(db: Database[dict[str, Any]]) -> None:
    token = create_session(db, "u1", ttl_days=14, now=NOW)
    docs = list(db.sessions.find())
    assert len(docs) == 1
    assert docs[0]["_id"] != token
    assert len(docs[0]["_id"]) == 64
    assert token not in str(docs[0])
    assert docs[0]["expires_at"] == NOW + timedelta(days=14)


def test_resolve_valid_session(db: Database[dict[str, Any]]) -> None:
    token = create_session(db, "u1", ttl_days=14, now=NOW)
    assert resolve_session(db, token, now=NOW + timedelta(days=1)) == "u1"
    assert resolve_session(db, "unknown", now=NOW) is None


def test_expired_session_is_rejected(db: Database[dict[str, Any]]) -> None:
    token = create_session(db, "u1", ttl_days=14, now=NOW)
    assert resolve_session(db, token, now=NOW + timedelta(days=14)) is None
    assert resolve_session(db, token, now=NOW + timedelta(days=15)) is None


def test_revoke_session(db: Database[dict[str, Any]]) -> None:
    token = create_session(db, "u1", ttl_days=14, now=NOW)
    revoke_session(db, token)
    assert resolve_session(db, token, now=NOW) is None


def test_revoke_user_sessions_counts(db: Database[dict[str, Any]]) -> None:
    create_session(db, "u1", ttl_days=14, now=NOW)
    create_session(db, "u1", ttl_days=14, now=NOW)
    other = create_session(db, "u2", ttl_days=14, now=NOW)
    assert revoke_user_sessions(db, "u1") == 2
    assert revoke_user_sessions(db, "u1") == 0
    assert resolve_session(db, other, now=NOW) == "u2"


def _cookie_header(settings: Settings, *, clear: bool = False) -> str:
    app = FastAPI()

    @app.get("/c")
    def _route(response: Response) -> dict[str, str]:
        if clear:
            clear_session_cookie(response)
        else:
            set_session_cookie(response, "tok", settings)
        return {}

    return TestClient(app).get("/c").headers["set-cookie"]


def test_cookie_flags(settings: Settings) -> None:
    header = _cookie_header(settings).lower()
    assert f"{SESSION_COOKIE}=tok" in header
    assert "httponly" in header
    assert "samesite=lax" in header
    assert "secure" not in header.replace("samesite", "")
    assert f"max-age={settings.session_ttl_days * 86400}" in header


def test_cookie_secure_follows_settings(settings: Settings) -> None:
    secure = settings.model_copy(update={"cookie_secure": True})
    assert "secure" in _cookie_header(secure).lower().replace("samesite", "")


def test_clear_cookie(settings: Settings) -> None:
    header = _cookie_header(settings, clear=True).lower()
    assert f"{SESSION_COOKIE}=" in header
    assert "max-age=0" in header
