from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

from .exceptions import ConfigurationError

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class Settings:
    github_token: str | None
    llm_provider: str
    llm_base_url: str | None
    llm_model: str
    llm_api_key: str | None
    rough_llm_model: str | None
    r2_endpoint_url: str | None
    r2_access_key_id: str | None
    r2_secret_access_key: str | None
    r2_bucket_name: str | None
    r2_cache_key: str
    state_backend: str
    local_state_path: Path
    hugo_content_dir: Path
    output_dir: Path
    max_candidates: int
    rough_screen_limit: int
    final_publish_limit: int
    score_threshold: float
    cache_ttl_days: int
    min_fork_star_ratio: float
    min_stars: int
    min_stars_week: int
    max_repo_age_days: int
    require_recent_push_hours: int
    dry_run: bool
    code_source: str
    max_code_files: int
    max_file_bytes: int
    max_total_code_chars: int
    min_code_files_for_audit: int
    git_clone_timeout_seconds: int

    @classmethod
    def from_env(cls) -> Settings:
        dry_run = _env_bool("REPOINTEL_DRY_RUN", default=False)
        root = Path(os.getenv("REPOINTEL_ROOT", ".")).resolve()
        settings = cls(
            github_token=_blank_to_none(os.getenv("GITHUB_TOKEN")),
            llm_provider=_default_if_blank(os.getenv("LLM_PROVIDER"), "openai").strip().lower(),
            llm_base_url=_blank_to_none(os.getenv("LLM_BASE_URL")),
            llm_model=os.getenv("LLM_MODEL", "").strip(),
            llm_api_key=_blank_to_none(os.getenv("LLM_API_KEY")),
            rough_llm_model=_blank_to_none(os.getenv("ROUGH_LLM_MODEL")),
            r2_endpoint_url=_blank_to_none(os.getenv("R2_ENDPOINT_URL")),
            r2_access_key_id=_blank_to_none(os.getenv("R2_ACCESS_KEY_ID")),
            r2_secret_access_key=_blank_to_none(os.getenv("R2_SECRET_ACCESS_KEY")),
            r2_bucket_name=_blank_to_none(os.getenv("R2_BUCKET_NAME")),
            r2_cache_key=os.getenv("R2_CACHE_KEY", "processed_repos.json").strip(),
            state_backend=os.getenv("REPOINTEL_STATE_BACKEND", "r2").strip().lower(),
            local_state_path=Path(
                os.getenv("REPOINTEL_LOCAL_STATE", root / "output" / "processed_repos.json")
            ),
            hugo_content_dir=Path(
                os.getenv("HUGO_CONTENT_DIR", root / "hugo-site" / "content" / "posts")
            ),
            output_dir=Path(os.getenv("REPOINTEL_OUTPUT_DIR", root / "output")),
            max_candidates=_env_int("REPOINTEL_MAX_CANDIDATES", 100),
            rough_screen_limit=_env_int("REPOINTEL_ROUGH_LIMIT", 15),
            final_publish_limit=_env_int("REPOINTEL_FINAL_LIMIT", 10),
            score_threshold=_env_float("REPOINTEL_SCORE_THRESHOLD", 75.0),
            cache_ttl_days=_env_int("REPOINTEL_CACHE_TTL_DAYS", 14),
            min_fork_star_ratio=_env_float("REPOINTEL_MIN_FORK_STAR_RATIO", 0.01),
            min_stars=_env_int("REPOINTEL_MIN_STARS", 300),
            min_stars_week=_env_int("REPOINTEL_MIN_STARS_WEEK", 100),
            max_repo_age_days=_env_int("REPOINTEL_MAX_REPO_AGE_DAYS", 30),
            require_recent_push_hours=_env_int("REPOINTEL_RECENT_PUSH_HOURS", 48),
            dry_run=dry_run,
            code_source=os.getenv("REPOINTEL_CODE_SOURCE", "auto").strip().lower(),
            max_code_files=_env_int("REPOINTEL_MAX_CODE_FILES", 48),
            max_file_bytes=_env_int("REPOINTEL_MAX_FILE_BYTES", 48_000),
            max_total_code_chars=_env_int("REPOINTEL_MAX_TOTAL_CODE_CHARS", 600_000),
            min_code_files_for_audit=_env_int("REPOINTEL_MIN_CODE_FILES", 5),
            git_clone_timeout_seconds=_env_int("REPOINTEL_GIT_CLONE_TIMEOUT", 300),
        )
        settings.validate()
        settings.log_safe_summary()
        return settings

    def validate(self) -> None:
        if self.llm_provider not in {"openai", "claude"}:
            raise ConfigurationError("LLM_PROVIDER must be either 'openai' or 'claude'.")
        if not self.dry_run:
            if not self.llm_model:
                raise ConfigurationError("LLM_MODEL is required unless REPOINTEL_DRY_RUN=true.")
            if not self.llm_api_key:
                raise ConfigurationError("LLM_API_KEY is required unless REPOINTEL_DRY_RUN=true.")
        if self.state_backend not in {"r2", "local"}:
            raise ConfigurationError("REPOINTEL_STATE_BACKEND must be either 'r2' or 'local'.")
        if self.state_backend == "r2" and not self.dry_run:
            missing = [
                name
                for name, value in {
                    "R2_ENDPOINT_URL": self.r2_endpoint_url,
                    "R2_ACCESS_KEY_ID": self.r2_access_key_id,
                    "R2_SECRET_ACCESS_KEY": self.r2_secret_access_key,
                    "R2_BUCKET_NAME": self.r2_bucket_name,
                }.items()
                if not value
            ]
            if missing:
                raise ConfigurationError(f"Missing R2 configuration: {', '.join(missing)}")
        if self.max_candidates <= 0:
            raise ConfigurationError("REPOINTEL_MAX_CANDIDATES must be positive.")
        if self.rough_screen_limit <= 0 or self.final_publish_limit <= 0:
            raise ConfigurationError("Screening and publish limits must be positive.")
        if self.rough_screen_limit > self.max_candidates:
            raise ConfigurationError(
                "REPOINTEL_ROUGH_LIMIT cannot exceed REPOINTEL_MAX_CANDIDATES."
            )
        if self.final_publish_limit > self.rough_screen_limit:
            raise ConfigurationError("REPOINTEL_FINAL_LIMIT cannot exceed REPOINTEL_ROUGH_LIMIT.")
        if not (0 <= self.score_threshold <= 100):
            raise ConfigurationError("REPOINTEL_SCORE_THRESHOLD must be between 0 and 100.")
        if self.cache_ttl_days <= 0 or self.require_recent_push_hours <= 0:
            raise ConfigurationError("Cache TTL and recent push window must be positive.")
        if self.min_stars < 0 or self.min_fork_star_ratio < 0:
            raise ConfigurationError("Minimum star and fork/star thresholds cannot be negative.")
        if self.min_stars_week < 0:
            raise ConfigurationError("REPOINTEL_MIN_STARS_WEEK cannot be negative.")
        if self.max_repo_age_days <= 0:
            raise ConfigurationError("REPOINTEL_MAX_REPO_AGE_DAYS must be positive.")
        if self.code_source not in {"auto", "git", "api"}:
            raise ConfigurationError("REPOINTEL_CODE_SOURCE must be auto, git, or api.")
        if self.max_code_files <= 0 or self.min_code_files_for_audit <= 0:
            raise ConfigurationError("Code file limits must be positive.")
        if self.min_code_files_for_audit > self.max_code_files:
            raise ConfigurationError("REPOINTEL_MIN_CODE_FILES cannot exceed REPOINTEL_MAX_CODE_FILES.")
        if self.max_file_bytes <= 0 or self.max_total_code_chars <= 0:
            raise ConfigurationError("Code size budgets must be positive.")

    def log_safe_summary(self) -> None:
        def _mask(value: str | None) -> str:
            if not value:
                return "<empty>"
            if len(value) <= 6:
                return "***"
            return f"{value[:4]}...{value[-4:]}"

        LOGGER.info(
            "RepoIntel config loaded: dry_run=%s, provider=%s, model=%s, rough_model=%s, "
            "github_token=%s, state_backend=%s, r2_endpoint=%s, r2_bucket=%s, r2_key=%s, "
            "max_candidates=%d, rough_limit=%d, final_limit=%d, score_threshold=%s, "
            "min_stars=%d, min_stars_week=%d, min_fork_star_ratio=%s, max_repo_age_days=%d, "
            "recent_push_hours=%d, cache_ttl_days=%d",
            self.dry_run,
            self.llm_provider,
            self.llm_model or "<empty>",
            self.rough_llm_model or "<same-as-deep-model>",
            _mask(self.github_token),
            self.state_backend,
            self.r2_endpoint_url or "<empty>",
            self.r2_bucket_name or "<empty>",
            self.r2_cache_key,
            self.max_candidates,
            self.rough_screen_limit,
            self.final_publish_limit,
            self.score_threshold,
            self.min_stars,
            self.min_stars_week,
            self.min_fork_star_ratio,
            self.max_repo_age_days,
            self.require_recent_push_hours,
            self.cache_ttl_days,
        )


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _default_if_blank(value: str | None, default: str) -> str:
    if value is None:
        return default
    stripped = value.strip()
    return stripped or default


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer.") from exc


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be a number.") from exc


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}
