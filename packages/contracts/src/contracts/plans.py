"""Execution plan contracts."""
from __future__ import annotations

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    """A single step in an execution plan."""

    step_id: str
    description: str
    file_paths: list[str] = Field(default_factory=list)
    estimated_complexity: float = Field(default=0.5, ge=0.0, le=1.0)


class ExecutionPlan(BaseModel):
    """Ordered list of steps produced by the planning agent."""

    task_id: str
    steps: list[PlanStep]
    schema_version: int = Field(default=1, ge=1)
