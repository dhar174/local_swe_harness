"""Unit tests for the model capability registry."""
from __future__ import annotations

import textwrap

import pytest
import yaml

from model_clients.capabilities import ModelCapability, ModelRole, ModelTier, ModelSpec
from model_clients.registry import ModelRegistry


pytestmark = pytest.mark.unit


SAMPLE_CONFIG = textwrap.dedent("""\
    models:
      - name: fast-coder-7b
        tier: tier1_fast
        roles: [coder, navigator]
        capabilities: [chat, code_completion]
        context_window: 8192
        backend: llamacpp
      - name: heavy-architect-34b
        tier: tier2_heavy
        roles: [architect, reviewer]
        capabilities: [chat, function_calling, long_context]
        context_window: 32768
        backend: ollama
""")


@pytest.fixture
def registry(tmp_path: pytest.TempPathFactory) -> ModelRegistry:
    cfg = tmp_path / "models.yaml"
    cfg.write_text(SAMPLE_CONFIG)
    return ModelRegistry.from_yaml(cfg)


def test_get_coder_tier1(registry: ModelRegistry) -> None:
    spec = registry.get_for_role(ModelRole.CODER, tier=ModelTier.TIER1_FAST)
    assert spec.name == "fast-coder-7b"


def test_get_architect_tier2(registry: ModelRegistry) -> None:
    spec = registry.get_for_role(ModelRole.ARCHITECT, tier=ModelTier.TIER2_HEAVY)
    assert spec.name == "heavy-architect-34b"


def test_missing_role_raises_key_error(registry: ModelRegistry) -> None:
    with pytest.raises(KeyError):
        registry.get_for_role(ModelRole.CLOUD_ENGINEER, tier=ModelTier.TIER1_FAST)


def test_all_specs_returns_all(registry: ModelRegistry) -> None:
    assert len(registry.all_specs()) == 2


def test_model_spec_schema_version_default() -> None:
    spec = ModelSpec(
        name="m",
        tier=ModelTier.TIER1_FAST,
        roles=[ModelRole.CODER],
        capabilities=[ModelCapability.CHAT],
    )
    assert spec.schema_version == 1
