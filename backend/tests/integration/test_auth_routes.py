import logging
from collections.abc import Callable
from typing import Any

import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from pymongo.database import Database

from app.auth.oauth import get_identity_resolver
from app.auth.sessions import SESSION_COOKIE
from app.auth.signup import OAuthIdentity
from app.errors import AppError

MakeUser = Callable[..., dict[str, Any]]

EMAIL = "a@example.com"
CALLBACK = "/api/auth/callback/google"


def use_identity(client: TestClient, identity: OAuthIdentity | None) -> None:
    """Troca o resolver real por um falso: devolve `identity`, ou falha se for None."""

    async def fake_resolver(provider: str, request: Request) -> OAuthIdentity:
        if identity is None:
            raise AppError("LOGIN_FAILED", "Could not sign in. Please try again.", 401)
        return identity

    client.app.dependency_overrides[get_identity_resolver] = lambda: fake_resolver  # type: ignore[attr-defined]


def test_callback_resolver_failure_redirects_login_failed(client: TestClient) -> None:
    use_identity(client, None)

    response = client.get(CALLBACK, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "http://localhost:4200/login?error=login_failed"


def test_callback_existing_active_user_logs_in(
    client: TestClient, make_user: MakeUser, caplog: pytest.LogCaptureFixture
) -> None:
    make_user(email=EMAIL)
    use_identity(client, OAuthIdentity("google", f"sub-{EMAIL}", EMAIL))
    caplog.set_level(logging.INFO)

    response = client.get(CALLBACK, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "http://localhost:4200/jobs"
    assert SESSION_COOKIE in response.cookies
    assert EMAIL not in caplog.text


def test_callback_inactive_user_login_failed(
    client: TestClient, make_user: MakeUser, db: Database[dict[str, Any]]
) -> None:
    make_user(email=EMAIL, active=False)
    use_identity(client, OAuthIdentity("google", f"sub-{EMAIL}", EMAIL))

    response = client.get(CALLBACK, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "http://localhost:4200/login?error=login_failed"
    assert SESSION_COOKIE not in response.cookies
    assert db.sessions.count_documents({}) == 0


def test_callback_not_invited_redirects_and_stores_no_user(
    client: TestClient, db: Database[dict[str, Any]]
) -> None:
    use_identity(client, OAuthIdentity("google", "sub-new", EMAIL))

    response = client.get(CALLBACK, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "http://localhost:4200/login?error=not_invited"
    assert db.users.count_documents({}) == 0
    attempt = db.signup_attempts.find_one()
    assert attempt is not None
    assert attempt["outcome"] == "rejected_not_invited"


def test_callback_invited_sets_pending_and_redirects_to_terms(
    client: TestClient, db: Database[dict[str, Any]]
) -> None:
    db.allowed_emails.insert_one({"_id": EMAIL})  # convida o e-mail
    use_identity(client, OAuthIdentity("google", "sub-new", EMAIL))

    response = client.get(CALLBACK, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "http://localhost:4200/signup/terms"
    assert "session" in response.cookies  # cookie do SessionMiddleware com o pending_signup
    assert db.users.count_documents({}) == 0  # ainda não cria usuário
    attempt = db.signup_attempts.find_one()
    assert attempt is not None
    assert attempt["outcome"] == "pending_terms"
