"""Minimal end-to-end example using fake models and a disposable fixture repo.

No real LLMs, no network calls. Verifies that the core routing and state
transition plumbing works end-to-end with deterministic fakes.
"""
from __future__ import annotations

import pytest

from contracts.state import Tier, TaskStatus
from contracts.tasks import Task, TaskRequest
from model_clients.fake import FakeModelClient
from model_clients.capabilities import ModelRole, ModelTier, ModelSpec, ModelCapability
from model_clients.registry import ModelRegistry
from swe_agents.routing.complexity import score_complexity
from swe_agents.routing.escalation import should_escalate, next_tier
from swe_agents.state import OrchestratorState


pytestmark = [pytest.mark.e2e]


def make_state(complexity: float = 0.2, attempt: int = 0) -> OrchestratorState:
    return OrchestratorState(
        task_id="e2e-001",
        thread_id="th-e2e",
        tier=Tier.TIER1_FAST,
        complexity_score=complexity,
        attempt=attempt,
    )


def test_low_complexity_stays_tier1() -> None:
    state = make_state(complexity=0.2)
    assert not should_escalate(state)
    assert state.tier == Tier.TIER1_FAST


def test_high_complexity_escalates_to_tier2() -> None:
    state = make_state(complexity=0.9)
    assert should_escalate(state)
    state.tier = next_tier(state.tier)
    assert state.tier == Tier.TIER2_HEAVY


def test_retry_exhaustion_escalates() -> None:
    state = make_state(attempt=3)
    assert should_escalate(state)


def test_fake_model_registry_routing() -> None:
    """Registry returns configuration-driven model for each role."""
    specs = [
        ModelSpec(
            name="fake-coder",
            tier=ModelTier.TIER1_FAST,
            roles=[ModelRole.CODER],
            capabilities=[ModelCapability.CHAT],
        ),
        ModelSpec(
            name="fake-reviewer",
            tier=ModelTier.TIER1_FAST,
            roles=[ModelRole.REVIEWER],
            capabilities=[ModelCapability.CHAT],
        ),
    ]
    registry = ModelRegistry(specs)
    coder_spec = registry.get_for_role(ModelRole.CODER)
    reviewer_spec = registry.get_for_role(ModelRole.REVIEWER)
    assert coder_spec.name == "fake-coder"
    assert reviewer_spec.name == "fake-reviewer"
