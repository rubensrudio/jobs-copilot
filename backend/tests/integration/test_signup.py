from datetime import UTC, datetime
from typing import Any

import pytest
from pymongo.database import Database

from app.auth.signup import (
    OAuthIdentity,
    create_user,
    find_user_by_identity,
    is_email_allowed,
    normalize_email,
    record_signup_attempt,
)
from app.config import Settings
from app.errors import AppError

NOW = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)


def _identity(
    email: str = "a@example.com", provider: str = "google", subject: str = "g-1"
) -> OAuthIdentity:
    return OAuthIdentity(provider=provider, subject=subject, email=email)


def _with_bootstrap(settings: Settings, *emails: str) -> Settings:
    return settings.model_copy(update={"bootstrap_admin_emails": list(emails)})


def test_normalize_email() -> None:
    assert normalize_email("  A@Example.COM ") == "a@example.com"


def test_email_not_in_list_is_not_allowed(db: Database[dict[str, Any]], settings: Settings) -> None:
    assert not is_email_allowed(db, "a@example.com", settings)


def test_invited_email_is_allowed_case_insensitive(
    db: Database[dict[str, Any]], settings: Settings
) -> None:
    db.allowed_emails.insert_one({"_id": "a@example.com", "added_at": NOW, "added_by": "x"})
    assert is_email_allowed(db, " A@Example.com ", settings)


def test_bootstrap_admin_is_allowed_and_admin(
    db: Database[dict[str, Any]], settings: Settings
) -> None:
    boot = _with_bootstrap(settings, "Boss@Example.com")
    assert is_email_allowed(db, "boss@example.com", boot)
    user = create_user(
        db, _identity("boss@example.com"), terms_version=boot.terms_version, settings=boot, now=NOW
    )
    assert user["role"] == "admin"


def test_attempt_stores_only_hash(db: Database[dict[str, Any]]) -> None:
    record_signup_attempt(db, " Secret@Example.com ", "github", "rejected_not_invited", NOW)
    docs = list(db.signup_attempts.find())
    assert len(docs) == 1
    doc = docs[0]
    assert set(doc) == {"_id", "email_sha256", "provider", "outcome", "at"}
    assert "secret@example.com" not in str(doc).lower()
    assert len(doc["email_sha256"]) == 64


def test_attempt_hash_is_normalized(db: Database[dict[str, Any]]) -> None:
    record_signup_attempt(db, "A@example.com", "google", "created", NOW)
    record_signup_attempt(db, " a@EXAMPLE.com", "google", "created", NOW)
    hashes = {d["email_sha256"] for d in db.signup_attempts.find()}
    assert len(hashes) == 1


def test_create_user_records_terms_version_and_time(
    db: Database[dict[str, Any]], settings: Settings
) -> None:
    user = create_user(
        db, _identity(), terms_version=settings.terms_version, settings=settings, now=NOW
    )
    stored = db.users.find_one({"_id": user["_id"]})
    assert stored is not None
    assert stored["terms_acceptances"][0]["version"] == settings.terms_version
    assert stored["terms_acceptances"][0]["accepted_at"] == NOW
    assert stored["role"] == "user"
    assert stored["active"] is True
    assert stored["deletion_pending"] is False
    assert stored["identities"] == [{"provider": "google", "subject": "g-1"}]


def test_create_user_rejects_wrong_terms_version(
    db: Database[dict[str, Any]], settings: Settings
) -> None:
    with pytest.raises(AppError) as exc:
        create_user(db, _identity(), terms_version="old", settings=settings, now=NOW)
    assert exc.value.code == "TERMS_VERSION_MISMATCH"
    assert exc.value.status_code == 409
    assert db.users.count_documents({}) == 0


def test_find_user_by_identity_exact_match(
    db: Database[dict[str, Any]], settings: Settings
) -> None:
    created = create_user(
        db, _identity(), terms_version=settings.terms_version, settings=settings, now=NOW
    )
    found = find_user_by_identity(db, _identity())
    assert found is not None
    assert found["_id"] == created["_id"]
    assert find_user_by_identity(db, _identity("other@example.com", subject="g-2")) is None


def test_find_user_links_second_provider(db: Database[dict[str, Any]], settings: Settings) -> None:
    created = create_user(
        db, _identity(), terms_version=settings.terms_version, settings=settings, now=NOW
    )
    gh = _identity("A@Example.com", provider="github", subject="gh-9")
    found = find_user_by_identity(db, gh)
    assert found is not None
    assert found["_id"] == created["_id"]
    assert {"provider": "github", "subject": "gh-9"} in found["identities"]
    assert len(found["identities"]) == 2
    find_user_by_identity(db, gh)
    stored = db.users.find_one({"_id": created["_id"]})
    assert stored is not None
    assert len(stored["identities"]) == 2


def test_new_user_default_settings(db: Database[dict[str, Any]], settings: Settings) -> None:
    user = create_user(
        db, _identity(), terms_version=settings.terms_version, settings=settings, now=NOW
    )
    assert user["settings"] == {
        "highlight_enabled": True,
        "highlight_threshold": 70,
        "cost_cap_usd": settings.default_user_cost_cap_usd,
    }
