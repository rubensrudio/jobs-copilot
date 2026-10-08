import hmac
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated, Any, Literal

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, Header, Request
from pymongo.database import Database

from app.auth.sessions import SESSION_COOKIE, resolve_session
from app.config import Settings, get_settings
from app.db import Collections, get_db
from app.errors import AppError


@dataclass(frozen=True)
class CurrentUser:
    id: str
    email: str
    role: Literal["user", "admin"]


def _unauthenticated() -> AppError:
    return AppError("UNAUTHENTICATED", "Please sign in.", 401)


def get_current_user(
    request: Request, db: Annotated[Database[dict[str, Any]], Depends(get_db)]
) -> CurrentUser:
    raw_token = request.cookies.get(SESSION_COOKIE)
    if not raw_token:
        raise _unauthenticated()
    user_id = resolve_session(db, raw_token, now=datetime.now(UTC))
    if user_id is None:
        raise _unauthenticated()
    try:
        object_id = ObjectId(user_id)
    except InvalidId:
        raise _unauthenticated() from None
    user = db[Collections.USERS].find_one({"_id": object_id})
    if user is None or not user.get("active") or user.get("deletion_pending"):
        raise _unauthenticated()
    return CurrentUser(id=user_id, email=user["email"], role=user["role"])


def require_admin(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    if user.role != "admin":
        raise AppError("FORBIDDEN", "Admin access required.", 403)
    return user


def require_collector_token(
    settings: Annotated[Settings, Depends(get_settings)],
    authorization: Annotated[str | None, Header()] = None,
) -> None:
    expected = settings.collector_token.get_secret_value()
    prefix = "Bearer "
    provided = ""
    if authorization and authorization.startswith(prefix):
        provided = authorization[len(prefix) :]
    if not expected or not hmac.compare_digest(provided.encode(), expected.encode()):
        raise AppError("INVALID_COLLECTOR_TOKEN", "Invalid collector token.", 401)
