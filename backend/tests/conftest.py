import os
from collections.abc import Callable, Iterator
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from pymongo.database import Database

from app.auth.sessions import SESSION_COOKIE, create_session
from app.config import Settings
from app.db import ensure_indexes, get_db
from app.main import create_app

FAKE_LONG_VALUE = "x" * 32


@pytest.fixture(scope="session")
def mongo_client() -> Iterator[MongoClient[dict[str, Any]]]:
    client: MongoClient[dict[str, Any]] = MongoClient(
        os.environ.get("MONGO_URI", "mongodb://localhost:27017"), tz_aware=True
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def test_db_name(mongo_client: MongoClient[dict[str, Any]]) -> Iterator[str]:
    name = f"jobs_copilot_test_{uuid4().hex}"
    yield name
    mongo_client.drop_database(name)


@pytest.fixture
def db(
    mongo_client: MongoClient[dict[str, Any]], test_db_name: str
) -> Iterator[Database[dict[str, Any]]]:
    database = mongo_client[test_db_name]
    ensure_indexes(database)
    yield database
    for name in database.list_collection_names():
        if not name.startswith("system."):
            database[name].delete_many({})


@pytest.fixture
def settings(test_db_name: str) -> Settings:
    return Settings(
        _env_file=None,
        mongo_db=test_db_name,
        session_secret=FAKE_LONG_VALUE,
        collector_token=FAKE_LONG_VALUE,
    )


@pytest.fixture
def client(settings: Settings, db: Database[dict[str, Any]]) -> TestClient:
    app = create_app(settings)
    app.dependency_overrides[get_db] = lambda: db
    return TestClient(app)


@pytest.fixture
def make_user(db: Database[dict[str, Any]]) -> Callable[..., dict[str, Any]]:
    def _make_user(
        email: str = "a@example.com",
        role: str = "user",
        active: bool = True,
        deletion_pending: bool = False,
    ) -> dict[str, Any]:
        user: dict[str, Any] = {
            "email": email,
            "identities": [{"provider": "google", "subject": f"sub-{email}"}],
            "role": role,
            "active": active,
            "created_at": datetime.now(UTC),
            "terms_acceptances": [],
            "settings": {
                "highlight_enabled": True,
                "highlight_threshold": 70,
                "cost_cap_usd": 5.0,
            },
            "deletion_pending": deletion_pending,
        }
        user["_id"] = db.users.insert_one(user).inserted_id
        return user

    return _make_user


@pytest.fixture
def login_as(
    db: Database[dict[str, Any]], settings: Settings
) -> Callable[[TestClient, dict[str, Any]], None]:
    def _login_as(client: TestClient, user: dict[str, Any]) -> None:
        token = create_session(
            db, str(user["_id"]), ttl_days=settings.session_ttl_days, now=datetime.now(UTC)
        )
        client.cookies.set(SESSION_COOKIE, token)

    return _login_as
