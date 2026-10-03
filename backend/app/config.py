from functools import lru_cache
from typing import Annotated, Any, Literal

from pydantic import SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

MIN_PRODUCTION_SECRET_LENGTH = 32


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        extra="ignore",
        env_ignore_empty=True,
    )

    # App
    env: Literal["development", "production"] = "development"
    frontend_url: str = "http://localhost:4200"
    cookie_secure: bool = False

    # MongoDB
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "jobs_copilot"

    # Session
    session_secret: SecretStr = SecretStr("")
    session_ttl_days: int = 14

    # OAuth
    google_client_id: str = ""
    google_client_secret: SecretStr = SecretStr("")
    github_client_id: str = ""
    github_client_secret: SecretStr = SecretStr("")

    # Admin bootstrap and terms
    bootstrap_admin_emails: Annotated[list[str], NoDecode] = []
    terms_version: str = "2026-10-01"

    # LLM
    openai_api_key: SecretStr = SecretStr("")
    llm_model: str = "gpt-4o-mini"
    llm_timeout_s: int = 25
    embedding_model: str = "text-embedding-3-small"
    llm_price_input_per_mtok: float = 0.15
    llm_price_output_per_mtok: float = 0.60
    embedding_price_per_mtok: float = 0.02

    # Pinecone and MLflow
    pinecone_api_key: SecretStr = SecretStr("")
    pinecone_index: str = "jobs-copilot"
    mlflow_tracking_uri: str = "http://localhost:5001"

    # Cost caps (USD)
    default_user_cost_cap_usd: float = 5.0
    default_global_cost_cap_usd: float = 50.0
    analysis_cost_estimate_usd: float = 0.05
    cv_cost_estimate_usd: float = 0.05

    # Analysis limits
    max_posting_chars: int = 30000
    analysis_timeout_s: int = 60

    # Collection
    collector_token: SecretStr = SecretStr("")
    greenhouse_boards: Annotated[list[str], NoDecode] = []

    @field_validator("bootstrap_admin_emails", "greenhouse_boards", mode="before")
    @classmethod
    def _split_csv(cls, value: Any) -> Any:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def _require_long_secrets_in_production(self) -> "Settings":
        if self.env != "production":
            return self
        for name in ("session_secret", "collector_token"):
            secret: SecretStr = getattr(self, name)
            if len(secret.get_secret_value()) < MIN_PRODUCTION_SECRET_LENGTH:
                raise ValueError(
                    f"{name} must have at least {MIN_PRODUCTION_SECRET_LENGTH} "
                    "characters in production"
                )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
