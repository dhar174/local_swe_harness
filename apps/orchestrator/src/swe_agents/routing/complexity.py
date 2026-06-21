"""Complexity scoring for routing decisions."""
from __future__ import annotations

from swe_agents.state import OrchestratorState


def score_complexity(state: OrchestratorState) -> float:
    """Return a complexity score in [0, 1] for the task in *state*.

    Complexity drives tier selection. High complexity (>0.7) triggers
    escalation to heavier tiers. Scoring is based on configurable heuristics;
    model-role assignments come from the registry, not from this function.
    """
    # Stub: real implementation measures file count, test coverage, etc.
    return state.complexity_score
