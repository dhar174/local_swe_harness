"""Shared test fixtures for orchestrator tests."""
from __future__ import annotations

import pytest

from contracts.state import Tier
from contracts.tasks import Task, TaskRequest
from model_clients.fake import FakeModelClient
from swe_agents.state import OrchestratorState


@pytest.fixture
def sample_task_request() -> TaskRequest:
    return TaskRequest(
        repository_url="https://github.com/example/repo",
        title="Fix null pointer in login",
        description="Users see a 500 when email is empty.",
    )


@pytest.fixture
def sample_task(sample_task_request: TaskRequest) -> Task:
    return Task(
        task_id="task-001",
        request=sample_task_request,
    )


@pytest.fixture
def initial_state(sample_task: Task) -> OrchestratorState:
    return OrchestratorState(
        task_id=sample_task.task_id,
        thread_id="thread-001",
        tier=Tier.TIER1_FAST,
        task=sample_task,
    )


@pytest.fixture
def fake_client() -> FakeModelClient:
    return FakeModelClient(responses=["Hello from fake model"])


@pytest.fixture
def fake_client_factory() -> type[FakeModelClient]:
    return FakeModelClient
