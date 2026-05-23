from __future__ import annotations

import json
import logging
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .config import Settings
from .exceptions import ExternalServiceError
from .models import ProcessedState, RepoAudit

LOGGER = logging.getLogger(__name__)


class StateStore:
    def load(self) -> ProcessedState:
        raise NotImplementedError

    def save(self, state: ProcessedState) -> None:
        raise NotImplementedError


class LocalStateStore(StateStore):
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> ProcessedState:
        if not self.path.exists():
            return {}
        with self.path.open("r", encoding="utf-8") as handle:
            return _parse_state(handle.read())

    def save(self, state: ProcessedState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(state, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")


class R2StateStore(StateStore):
    def __init__(self, settings: Settings) -> None:
        if not all(
            [
                settings.r2_endpoint_url,
                settings.r2_access_key_id,
                settings.r2_secret_access_key,
                settings.r2_bucket_name,
            ]
        ):
            raise ExternalServiceError("R2 configuration is incomplete.")
        try:
            import boto3
            from botocore.exceptions import BotoCoreError, ClientError
        except ImportError as exc:
            raise ExternalServiceError(
                "boto3 is required for Cloudflare R2 state storage."
            ) from exc
        self._boto_core_error = BotoCoreError
        self._client_error = ClientError
        self.bucket = settings.r2_bucket_name
        self.key = settings.r2_cache_key
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.r2_endpoint_url,
            aws_access_key_id=settings.r2_access_key_id,
            aws_secret_access_key=settings.r2_secret_access_key,
            region_name="auto",
        )

    def load(self) -> ProcessedState:
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=self.key)
            body = response["Body"].read().decode("utf-8")
            return _parse_state(body)
        except self._client_error as exc:
            code = exc.response.get("Error", {}).get("Code")
            if code in {"NoSuchKey", "NoSuchBucket", "404"}:
                LOGGER.info("R2 state file does not exist yet; starting with empty state")
                return {}
            raise ExternalServiceError(f"Failed to load R2 state: {code}") from exc
        except self._boto_core_error as exc:
            raise ExternalServiceError("Failed to load R2 state.") from exc

    def save(self, state: ProcessedState) -> None:
        body = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=self.key,
                Body=body,
                ContentType="application/json; charset=utf-8",
            )
        except (self._client_error, self._boto_core_error) as exc:
            raise ExternalServiceError("Failed to save R2 state.") from exc


def build_state_store(settings: Settings) -> StateStore:
    if settings.dry_run or settings.state_backend == "local":
        return LocalStateStore(settings.local_state_path)
    return R2StateStore(settings)


def merge_audits_into_state(
    state: ProcessedState,
    audits: list[RepoAudit],
    *,
    now: datetime | None = None,
    ttl_days: int = 14,
) -> ProcessedState:
    now = now or datetime.now(UTC)
    cutoff = now.date() - timedelta(days=ttl_days)
    merged: ProcessedState = {}
    for repo_name, record in state.items():
        audited_at = str(record.get("audited_at", ""))
        try:
            if datetime.fromisoformat(audited_at).date() >= cutoff:
                merged[repo_name] = dict(record)
        except ValueError:
            continue
    for audit in audits:
        merged[audit.repo_name] = audit.to_cache_record(now)
    return merged


def _parse_state(raw: str) -> ProcessedState:
    if not raw.strip():
        return {}
    payload = json.loads(raw)
    if isinstance(payload, list):
        normalized: ProcessedState = {}
        for item in payload:
            if isinstance(item, dict) and item.get("repo_name"):
                normalized[str(item["repo_name"])] = item
            elif isinstance(item, str):
                normalized[item] = {"repo_name": item, "audited_at": "1970-01-01"}
        return normalized
    if isinstance(payload, dict):
        return {str(key): dict(value) for key, value in payload.items() if isinstance(value, dict)}
    raise ExternalServiceError("processed_repos.json must be a JSON object or list.")
