"""Structured observability event contract.

Every event emitted by the system must conform to this schema.
Sensitive fields are redacted before serialization.
"""
from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator


_REDACTED = "<redacted>"
_SENSITIVE_KEYS = frozenset({"api_key", "token", "secret", "password", "credential"})


class EventOutcome(str, enum.Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    RETRY = "retry"
    ESCALATED = "escalated"
    SKIPPED = "skipped"


class ObservabilityEvent(BaseModel):
    """Structured event emitted at each significant system action."""

    event_id: str
    task_id: str
    thread_id: str
    tier: str
    role: str  # e.g. router | coder | reviewer
    model: str
    node: str
    attempt: int = Field(default=0, ge=0)
    outcome: EventOutcome
    latency_ms: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost_usd: float | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict)
    schema_version: int = Field(default=1, ge=1)

    @field_validator("metadata", mode="before")
    @classmethod
    def redact_sensitive(cls, v: dict[str, Any]) -> dict[str, Any]:
        return {
            k: (_REDACTED if k.lower() in _SENSITIVE_KEYS else val)
            for k, val in v.items()
        }
