from collections.abc import Callable
from typing import Annotated, Any

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from pymongo.database import Database

from app.deps import CurrentUser, get_current_user, require_admin, require_collector_token
from app.main import create_app
from tests.conftest import FAKE_LONG_VALUE

MakeUser = Callable[..., dict[str, Any]]
LoginAs = Callable[[TestClient, dict[str, Any]], None]


@pytest.fixture
def test_client(client: TestClient) -> TestClient:
    app = client.app

    @app.get("/api/_test/me")  # type: ignore[attr-defined]
    def _me(user: Annotated[CurrentUser, Depends(get_current_user)]) -> dict[str, str]:
        return {"id": user.id, "email": user.email, "role": user.role}

    @app.get("/api/_test/admin")  # type: ignore[attr-defined]
    def _admin(user: Annotated[CurrentUser, Depends(require_admin)]) -> dict[str, str]:
        return {"id": user.id}

    @app.get("/api/_test/collector", dependencies=[Depends(require_collector_token)])  # type: ignore[attr-defined]
    def _collector() -> dict[str, bool]:
        return {"ok": True}

    return client


def test_valid_session_returns_current_user(
    test_client: TestClient, make_user: MakeUser, login_as: LoginAs
) -> None:
    user = make_user()
    login_as(test_client, user)
    response = test_client.get("/api/_test/me")
    assert response.status_code == 200
    assert response.json() == {"id": str(user["_id"]), "email": "a@example.com", "role": "user"}


def test_missing_cookie_401(test_client: TestClient) -> None:
    response = test_client.get("/api/_test/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHENTICATED"
    assert response.json()["error"]["message"] == "Please sign in."


def test_unknown_token_401(test_client: TestClient) -> None:
    test_client.cookies.set("jc_session", "not-a-real-token")
    assert test_client.get("/api/_test/me").status_code == 401


def test_inactive_user_401_even_with_session(
    test_client: TestClient, make_user: MakeUser, login_as: LoginAs, db: Database[dict[str, Any]]
) -> None:
    user = make_user()
    login_as(test_client, user)
    db.users.update_one({"_id": user["_id"]}, {"$set": {"active": False}})
    assert test_client.get("/api/_test/me").status_code == 401


def test_deletion_pending_user_401(
    test_client: TestClient, make_user: MakeUser, login_as: LoginAs
) -> None:
    login_as(test_client, make_user(deletion_pending=True))
    assert test_client.get("/api/_test/me").status_code == 401


def test_deleted_user_401(
    test_client: TestClient, make_user: MakeUser, login_as: LoginAs, db: Database[dict[str, Any]]
) -> None:
    user = make_user()
    login_as(test_client, user)
    db.users.delete_one({"_id": user["_id"]})
    assert test_client.get("/api/_test/me").status_code == 401


def test_require_admin_403_for_user(
    test_client: TestClient, make_user: MakeUser, login_as: LoginAs
) -> None:
    login_as(test_client, make_user())
    response = test_client.get("/api/_test/admin")
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


def test_require_admin_ok_for_admin(
    test_client: TestClient, make_user: MakeUser, login_as: LoginAs
) -> None:
    login_as(test_client, make_user(email="admin@example.com", role="admin"))
    assert test_client.get("/api/_test/admin").status_code == 200


def test_collector_token_ok_and_wrong(test_client: TestClient) -> None:
    ok = test_client.get(
        "/api/_test/collector", headers={"Authorization": f"Bearer {FAKE_LONG_VALUE}"}
    )
    assert ok.status_code == 200
    for headers in ({"Authorization": "Bearer wrong"}, {"Authorization": FAKE_LONG_VALUE}, {}):
        bad = test_client.get("/api/_test/collector", headers=headers)
        assert bad.status_code == 401
        assert bad.json()["error"]["code"] == "INVALID_COLLECTOR_TOKEN"


def test_collector_token_unset_rejects_empty_bearer() -> None:
    from app.config import Settings

    app = create_app(Settings(_env_file=None, collector_token=""))  # type: ignore[arg-type]

    @app.get("/c", dependencies=[Depends(require_collector_token)])
    def _c() -> dict[str, bool]:
        return {}

    assert TestClient(app).get("/c", headers={"Authorization": "Bearer "}).status_code == 401
