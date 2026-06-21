"""Root pytest configuration and shared fixtures."""
from __future__ import annotations

import pytest


@pytest.fixture
def fake_model_responses() -> list[str]:
    """Default fake model responses for deterministic tests."""
    return [
        '{"action": "plan", "steps": []}',
        '{"action": "code", "patches": []}',
        '{"action": "review", "approved": true}',
    ]
