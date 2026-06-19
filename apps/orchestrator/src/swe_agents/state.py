"""Extended LangGraph state for the orchestrator."""
from __future__ import annotations

from typing import Any

from contracts.plans import ExecutionPlan
from contracts.patches import PatchSet
from contracts.reviews import ReviewResult
from contracts.state import AgentState, TaskStatus, Tier
from contracts.tasks import Task
from contracts.verification import VerificationResult
from pydantic import Field


class OrchestratorState(AgentState):
    """Full orchestrator state passed through the LangGraph nodes."""

    task: Task | None = None
    plan: ExecutionPlan | None = None
    patch_set: PatchSet | None = None
    review_result: ReviewResult | None = None
    verification_result: VerificationResult | None = None
    error_log: list[str] = Field(default_factory=list)
    context_files: list[str] = Field(default_factory=list)
    complexity_score: float = Field(default=0.0, ge=0.0, le=1.0)
    escalation_reason: str | None = None

    # Routing decisions
    assigned_model: str | None = None  # Set by router from registry, NOT hardcoded
    next_node: str | None = None
