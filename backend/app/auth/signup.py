import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pymongo.database import Database

from app.config import Settings
from app.db import Collections
from app.errors import AppError


@dataclass
class OAuthIdentity:
    provider: str
    subject: str
    email: str


def normalize_email(email: str) -> str:
    return email.strip().lower()


def _is_bootstrap_admin(email: str, settings: Settings) -> bool:
    return email in {normalize_email(item) for item in settings.bootstrap_admin_emails}


def is_email_allowed(db: Database[dict[str, Any]], email: str, settings: Settings) -> bool:
    normalized = normalize_email(email)
    if _is_bootstrap_admin(normalized, settings):
        return True
    return db[Collections.ALLOWED_EMAILS].find_one({"_id": normalized}) is not None


def record_signup_attempt(
    db: Database[dict[str, Any]], email: str, provider: str, outcome: str, now: datetime
) -> None:
    db[Collections.SIGNUP_ATTEMPTS].insert_one(
        {
            "email_sha256": hashlib.sha256(normalize_email(email).encode()).hexdigest(),
            "provider": provider,
            "outcome": outcome,
            "at": now,
        }
    )


def find_user_by_identity(
    db: Database[dict[str, Any]], identity: OAuthIdentity
) -> dict[str, Any] | None:
    users = db[Collections.USERS]
    entry = {"provider": identity.provider, "subject": identity.subject}
    user = users.find_one({"identities": {"$elemMatch": entry}})
    if user is not None:
        return user
    user = users.find_one({"email": normalize_email(identity.email)})
    if user is None:
        return None
    users.update_one({"_id": user["_id"]}, {"$addToSet": {"identities": entry}})
    return users.find_one({"_id": user["_id"]})


def create_user(
    db: Database[dict[str, Any]],
    identity: OAuthIdentity,
    *,
    terms_version: str,
    settings: Settings,
    now: datetime,
) -> dict[str, Any]:
    if terms_version != settings.terms_version:
        raise AppError(
            "TERMS_VERSION_MISMATCH",
            "The terms of use have changed. Please review and accept the current version.",
            409,
        )
    email = normalize_email(identity.email)
    user: dict[str, Any] = {
        "email": email,
        "identities": [{"provider": identity.provider, "subject": identity.subject}],
        "role": "admin" if _is_bootstrap_admin(email, settings) else "user",
        "active": True,
        "created_at": now,
        "terms_acceptances": [{"version": terms_version, "accepted_at": now}],
        "settings": {
            "highlight_enabled": True,
            "highlight_threshold": 70,
            "cost_cap_usd": settings.default_user_cost_cap_usd,
        },
        "deletion_pending": False,
    }
    user["_id"] = db[Collections.USERS].insert_one(user).inserted_id
    return user
