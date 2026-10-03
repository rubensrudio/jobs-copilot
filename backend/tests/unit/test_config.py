import pytest
from pydantic import ValidationError

from app.config import Settings

SHORT_VALUE = "short"
LONG_VALUE = "x" * 32
FAKE_SESSION_VALUE = "fake-session-value"
FAKE_OPENAI_VALUE = "sk-test-123"
FAKE_COLLECTOR_VALUE = "fake-collector-value"


def test_defaults_match_plan() -> None:
    settings = Settings(_env_file=None)

    assert settings.default_user_cost_cap_usd == 5.0
    assert settings.default_global_cost_cap_usd == 50.0
    assert settings.max_posting_chars == 30000
    assert settings.analysis_timeout_s == 60
    assert settings.session_ttl_days == 14
    assert not any("threshold" in name for name in Settings.model_fields)


def test_csv_lists_are_parsed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOOTSTRAP_ADMIN_EMAILS", "a@x.com, b@y.com")
    monkeypatch.setenv("GREENHOUSE_BOARDS", "acme,,globex ")

    settings = Settings(_env_file=None)

    assert settings.bootstrap_admin_emails == ["a@x.com", "b@y.com"]
    assert settings.greenhouse_boards == ["acme", "globex"]


def test_secrets_are_not_in_repr() -> None:
    settings = Settings(
        _env_file=None,
        session_secret=FAKE_SESSION_VALUE,
        openai_api_key=FAKE_OPENAI_VALUE,
        collector_token=FAKE_COLLECTOR_VALUE,
    )

    text = repr(settings) + str(settings)

    assert FAKE_SESSION_VALUE not in text
    assert FAKE_OPENAI_VALUE not in text
    assert FAKE_COLLECTOR_VALUE not in text


def test_production_requires_long_secrets() -> None:
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            env="production",
            session_secret=SHORT_VALUE,
            collector_token=LONG_VALUE,
        )

    settings = Settings(
        _env_file=None,
        env="production",
        session_secret=LONG_VALUE,
        collector_token=LONG_VALUE,
    )
    assert settings.env == "production"