class RepoIntelError(Exception):
    """Base exception for RepoIntel failures."""


class ConfigurationError(RepoIntelError):
    """Raised when required runtime configuration is missing or invalid."""


class ExternalServiceError(RepoIntelError):
    """Raised when an upstream API or storage service fails."""


class LLMResponseError(RepoIntelError):
    """Raised when an LLM response cannot be parsed or validated."""
