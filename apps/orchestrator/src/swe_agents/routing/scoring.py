"""Composite task scoring helpers."""
from __future__ import annotations

from swe_agents.state import OrchestratorState


def composite_score(state: OrchestratorState) -> float:
    """Combine complexity and retry count into a routing score."""
    retry_penalty = min(state.attempt * 0.15, 0.45)
    return min(state.complexity_score + retry_penalty, 1.0)
