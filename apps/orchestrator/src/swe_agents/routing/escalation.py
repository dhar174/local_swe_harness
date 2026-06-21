"""Escalation decision logic."""
from __future__ import annotations

from contracts.state import Tier
from swe_agents.state import OrchestratorState


def should_escalate(state: OrchestratorState) -> bool:
    """Return True if the current task should be escalated to a higher tier."""
    if state.attempt >= 3:
        return True
    if state.complexity_score > 0.85:
        return True
    return False


def next_tier(current: Tier) -> Tier:
    """Return the next tier up from *current*."""
    order = [Tier.TIER1_FAST, Tier.TIER2_HEAVY, Tier.TIER3_CLOUD]
    idx = order.index(current)
    return order[min(idx + 1, len(order) - 1)]
