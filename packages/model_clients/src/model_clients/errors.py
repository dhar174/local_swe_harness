"""Model client error hierarchy."""
from __future__ import annotations


class ModelClientError(Exception):
    """Base class for model client errors."""


class ModelNotAvailableError(ModelClientError):
    """Raised when the requested model cannot be reached."""


class ModelRateLimitError(ModelClientError):
    """Raised on rate limit / quota exhaustion."""


class ModelContextLengthError(ModelClientError):
    """Raised when the prompt exceeds the model's context window."""
