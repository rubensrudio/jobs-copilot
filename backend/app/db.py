from functools import lru_cache
from typing import Any

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.database import Database

from app.config import Settings, get_settings


class Collections:
    USERS = "users"
    ALLOWED_EMAILS = "allowed_emails"
    SIGNUP_ATTEMPTS = "signup_attempts"
    SESSIONS = "sessions"
    PROFILES = "profiles"
    PROFILE_DRAFTS = "profile_drafts"
    FS_FILES = "fs.files"
    JOBS = "job_postings"
    ANALYSES = "analyses"
    TAILORED_CVS = "tailored_cvs"
    DECISIONS = "decisions"
    APPLICATIONS = "applications"
    SEARCH_CRITERIA = "search_criteria"
    COLLECTION_RUNS = "collection_runs"
    LOCKS = "locks"
    COST_LEDGERS = "cost_ledgers"
    COST_EVENTS = "cost_events"
    SETTINGS = "settings"
    RANKING_MODELS = "ranking_models"


USER_SCOPED_COLLECTIONS: tuple[str, ...] = (
    Collections.PROFILES,
    Collections.PROFILE_DRAFTS,
    Collections.JOBS,
    Collections.ANALYSES,
    Collections.TAILORED_CVS,
    Collections.DECISIONS,
    Collections.APPLICATIONS,
    Collections.SEARCH_CRITERIA,
    Collections.COST_EVENTS,
    Collections.COST_LEDGERS,
    Collections.SESSIONS,
    Collections.RANKING_MODELS,
)


@lru_cache
def _client_for(uri: str) -> MongoClient[dict[str, Any]]:
    return MongoClient(uri, tz_aware=True)


def get_client(settings: Settings) -> MongoClient[dict[str, Any]]:
    return _client_for(settings.mongo_uri)


def get_db() -> Database[dict[str, Any]]:
    settings = get_settings()
    return get_client(settings)[settings.mongo_db]


def ensure_indexes(db: Database[dict[str, Any]]) -> None:
    users = db[Collections.USERS]
    users.create_index("email", name="users_email_unique", unique=True)
    users.create_index(
        [("identities.provider", ASCENDING), ("identities.subject", ASCENDING)],
        name="users_identity_unique",
        unique=True,
    )

    db[Collections.SIGNUP_ATTEMPTS].create_index(
        "email_sha256", name="signup_attempts_email_sha256"
    )

    sessions = db[Collections.SESSIONS]
    sessions.create_index("expires_at", name="sessions_expires_at_ttl", expireAfterSeconds=0)
    sessions.create_index("user_id", name="sessions_user_id")

    db[Collections.FS_FILES].create_index("metadata.user_id", name="fs_files_user_id")

    jobs = db[Collections.JOBS]
    jobs.create_index(
        [("user_id", ASCENDING), ("normalized_url", ASCENDING)],
        name="jobs_user_url_unique",
        unique=True,
    )
    jobs.create_index(
        [("user_id", ASCENDING), ("source", ASCENDING), ("source_job_id", ASCENDING)],
        name="jobs_user_source_job_unique",
        unique=True,
        partialFilterExpression={"source_job_id": {"$exists": True}},
    )
    jobs.create_index(
        [("user_id", ASCENDING), ("skipped", ASCENDING), ("fit_score", DESCENDING)],
        name="jobs_user_skipped_fit_score",
    )

    db[Collections.ANALYSES].create_index(
        [("user_id", ASCENDING), ("job_id", ASCENDING), ("created_at", DESCENDING)],
        name="analyses_user_job_created_at",
    )
    db[Collections.TAILORED_CVS].create_index(
        [("user_id", ASCENDING), ("job_id", ASCENDING), ("version", ASCENDING)],
        name="tailored_cvs_user_job_version_unique",
        unique=True,
    )
    db[Collections.DECISIONS].create_index(
        [("user_id", ASCENDING), ("job_id", ASCENDING), ("created_at", DESCENDING)],
        name="decisions_user_job_created_at",
    )
    db[Collections.APPLICATIONS].create_index(
        [("user_id", ASCENDING), ("job_id", ASCENDING)],
        name="applications_user_job_unique",
        unique=True,
    )
    db[Collections.COLLECTION_RUNS].create_index(
        [("started_at", DESCENDING)], name="collection_runs_started_at"
    )
    db[Collections.COST_LEDGERS].create_index("user_id", name="cost_ledgers_user_id")
    db[Collections.COST_EVENTS].create_index(
        [("user_id", ASCENDING), ("at", DESCENDING)], name="cost_events_user_at"
    )
