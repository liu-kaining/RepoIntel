from __future__ import annotations

import pytest

from repointel.config import Settings
from repointel.exceptions import ConfigurationError


def test_settings_dry_run_allows_missing_llm_and_r2(monkeypatch) -> None:
    monkeypatch.setenv("REPOINTEL_DRY_RUN", "true")
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    settings = Settings.from_env()
    assert settings.dry_run is True


def test_settings_rejects_invalid_provider(monkeypatch) -> None:
    monkeypatch.setenv("REPOINTEL_DRY_RUN", "true")
    monkeypatch.setenv("LLM_PROVIDER", "bad")
    with pytest.raises(ConfigurationError):
        Settings.from_env()
