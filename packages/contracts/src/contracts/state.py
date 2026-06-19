"""Shared state types for the orchestrator graphs."""
from __future__ import annotations

import enum
from typing import Any

from pydantic import BaseModel, Field


class Tier(str, enum.Enum):
    """Model execution tier."""

    TIER1_FAST = "tier1_fast"
    TIER2_HEAVY = "tier2_heavy"
    TIER3_CLOUD = "tier3_cloud"


class TaskStatus(str, enum.Enum):
    """Task lifecycle status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"
    ABANDONED = "abandoned"


class AgentState(BaseModel):
    """Base LangGraph state shared across all graph nodes."""

    model_config = {"arbitrary_types_allowed": True}

    task_id: str = Field(..., description="Unique task identifier")
    thread_id: str = Field(..., description="LangGraph thread / checkpoint ID")
    tier: Tier = Field(default=Tier.TIER1_FAST)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    attempt: int = Field(default=0, ge=0)
    messages: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    # Schema version – bumped on every breaking state change
    schema_version: int = Field(default=1, ge=1)
