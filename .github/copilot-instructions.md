# GitHub Copilot Instructions

## Architecture Boundaries

This is a **monorepo** with strict dependency directions:

```
contracts  (no internal deps)
    ↑
model_clients, tool_clients
    ↑
swe_agents (orchestrator)
```

**Service packages** (`model_gateway`, `sandbox_worker`, `repo_indexer`) must NOT import `swe_agents`.

## Model Assignment Rules

**NEVER hardcode model names in graph nodes or agent code.**
Model assignments are **configuration-driven** via `config/models.yaml` and loaded through `ModelRegistry`.

```python
# WRONG – hardcoded model name
response = await client.complete("qwen2.5-coder-7b-instruct", messages)

# CORRECT – registry-driven
spec = registry.get_for_role(ModelRole.CODER, tier=Tier.TIER1_FAST)
response = await client.complete(spec.name, messages)
```

## Safety Rules

1. **Sandbox trust boundary**: The orchestrator NEVER executes arbitrary code directly. All code execution goes through the sandbox worker via `SandboxClient`.
2. **Command allowlist**: Only commands in `config/security.yaml:allowed_commands` may be submitted to the sandbox.
3. **Path allowlist**: All file access must be within `config/security.yaml:allowed_paths`.
4. **Prompt injection**: Strip system-role overrides from user content before passing to models.
5. **Secrets**: Never log or emit API keys, tokens, or passwords. Use `redact_dict()` / `redact_string()` before any logging.
6. **Destructive actions**: Actions in `config/security.yaml:destructive_actions_require_approval` must go through the approval flow.

## Required Checks

Before any commit:
- `make fmt-check` – formatting
- `make lint` – Ruff linting
- `make typecheck` – strict Mypy
- `make test-unit` – unit tests
- `make test-graph` – graph routing tests (fake models only)

## Coding Conventions

- All public functions must have full type annotations.
- Use `pydantic.BaseModel` for all data contracts.
- Every `BaseModel` that may be persisted must include `schema_version: int = Field(default=1, ge=1)`.
- Observability events must use `contracts.events.ObservabilityEvent` and call `redact_dict()` on metadata.
- Tests use `pytest.mark.unit`, `pytest.mark.graph`, `pytest.mark.integration`, `pytest.mark.e2e`, or `pytest.mark.llm`. Tests marked `llm` must NEVER run in normal CI.
- New packages belong in `packages/`; new services in `services/`; the orchestrator app in `apps/orchestrator/`.

## Versioning Requirements

Bump `schema_version` whenever a persisted schema changes in a backward-incompatible way:
- `AgentState` and subclasses
- `ObservabilityEvent`
- `config/models.yaml`
- `config/routing.yaml`
- Prompt templates in `prompts/` (use a comment header)
- Evaluation datasets in `evals/datasets/`
