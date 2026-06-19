"""Unit tests for routing complexity scoring and escalation."""
from __future__ import annotations

import pytest

from contracts.state import Tier
from swe_agents.routing.complexity import score_complexity
from swe_agents.routing.escalation import next_tier, should_escalate
from swe_agents.routing.scoring import composite_score
from swe_agents.state import OrchestratorState


pytestmark = pytest.mark.unit


@pytest.fixture
def base_state() -> OrchestratorState:
    return OrchestratorState(
        task_id="t1",
        thread_id="th1",
        complexity_score=0.3,
    )


def test_score_complexity_returns_state_score(base_state: OrchestratorState) -> None:
    assert score_complexity(base_state) == 0.3


def test_should_not_escalate_low_complexity(base_state: OrchestratorState) -> None:
    assert not should_escalate(base_state)


def test_should_escalate_after_3_attempts(base_state: OrchestratorState) -> None:
    base_state.attempt = 3
    assert should_escalate(base_state)


def test_should_escalate_high_complexity(base_state: OrchestratorState) -> None:
    base_state.complexity_score = 0.9
    assert should_escalate(base_state)


def test_next_tier_fast_to_heavy() -> None:
    assert next_tier(Tier.TIER1_FAST) == Tier.TIER2_HEAVY


def test_next_tier_heavy_to_cloud() -> None:
    assert next_tier(Tier.TIER2_HEAVY) == Tier.TIER3_CLOUD


def test_next_tier_cloud_stays_cloud() -> None:
    assert next_tier(Tier.TIER3_CLOUD) == Tier.TIER3_CLOUD


def test_composite_score_adds_retry_penalty(base_state: OrchestratorState) -> None:
    base_state.attempt = 2
    score = composite_score(base_state)
    assert score == pytest.approx(0.3 + 0.30, abs=1e-6)


def test_composite_score_caps_at_one(base_state: OrchestratorState) -> None:
    base_state.complexity_score = 0.9
    base_state.attempt = 5
    assert composite_score(base_state) <= 1.0
