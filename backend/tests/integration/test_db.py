from typing import Any

import pytest
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from app.db import USER_SCOPED_COLLECTIONS, Collections, ensure_indexes

DB = Database[dict[str, Any]]


def test_ensure_indexes_is_idempotent(db: DB) -> None:
    ensure_indexes(db)

    indexes = db[Collections.JOBS].index_information()
    assert "jobs_user_url_unique" in indexes
    assert "jobs_user_source_job_unique" in indexes


def test_job_url_unique_per_user(db: DB) -> None:
    jobs = db[Collections.JOBS]
    jobs.insert_one({"user_id": "u1", "normalized_url": "https://example.com/job/1"})

    with pytest.raises(DuplicateKeyError):
        jobs.insert_one({"user_id": "u1", "normalized_url": "https://example.com/job/1"})

    jobs.insert_one({"user_id": "u2", "normalized_url": "https://example.com/job/1"})
    assert jobs.count_documents({}) == 2


def test_source_job_id_partial_unique(db: DB) -> None:
    jobs = db[Collections.JOBS]
    jobs.insert_one({"user_id": "u1", "source": "manual", "normalized_url": "https://a.com/1"})
    jobs.insert_one({"user_id": "u1", "source": "manual", "normalized_url": "https://a.com/2"})
    jobs.insert_one(
        {
            "user_id": "u1",
            "source": "remotive",
            "source_job_id": "42",
            "normalized_url": "https://a.com/3",
        }
    )

    with pytest.raises(DuplicateKeyError):
        jobs.insert_one(
            {
                "user_id": "u1",
                "source": "remotive",
                "source_job_id": "42",
                "normalized_url": "https://a.com/4",
            }
        )


def test_sessions_ttl_index_exists(db: DB) -> None:
    indexes = db[Collections.SESSIONS].index_information()

    ttl = indexes["sessions_expires_at_ttl"]
    assert ttl["key"] == [("expires_at", 1)]
    assert ttl["expireAfterSeconds"] == 0


def test_user_scoped_collections_match_plan() -> None:
    assert set(USER_SCOPED_COLLECTIONS) == {
        "profiles",
        "profile_drafts",
        "job_postings",
        "analyses",
        "tailored_cvs",
        "decisions",
        "applications",
        "search_criteria",
        "cost_events",
        "cost_ledgers",
        "sessions",
        "ranking_models",
    }
    assert len(USER_SCOPED_COLLECTIONS) == 12
