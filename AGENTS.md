# AGENTS.md – Architecture, Safety Rules & Coding Conventions

## Overview

`tiered-swe-agents` is a LangGraph multi-agent system that routes coding tasks
across three execution tiers:

| Tier | Name | When |
|------|------|------|
| 1 | Fast Local | Simple, well-scoped tasks (complexity ≤ 0.5) |
| 2 | Heavy Local | Complex refactors, large context (complexity ≤ 0.85) |
| 3 | Cloud | Ambiguous, risky, or repeatedly-failing tasks |

## Monorepo Layout

```
packages/contracts/      – Shared typed data schemas (no internal deps)
packages/model_clients/  – Model capability registry, fake clients
packages/tool_clients/   – Tool interfaces (sandbox, repo, search)
apps/orchestrator/       – LangGraph graphs, nodes, agents, routing
services/model_gateway/  – Capability registry + backend adapters
services/sandbox_worker/ – Sandboxed code execution
services/repo_indexer/   – Symbol and dependency indexing
config/                  – YAML configuration (models, routing, security)
evals/                   – Evaluation harness and datasets
```

## Dependency Directions (enforced by architecture tests)

```
contracts  ← no internal imports
    ↑
model_clients, tool_clients
    ↑
swe_agents (graphs, nodes, agents, routing)
```

**Service packages must not import `swe_agents`.**
Violations are caught by `tests/test_architecture.py`.

## Model Assignment Rules

**Model names MUST NOT be hardcoded in graph nodes or agent code.**

All model assignments are configuration-driven via `config/models.yaml`
and accessed through `ModelRegistry`:

```python
from model_clients.registry import ModelRegistry
from model_clients.capabilities import ModelRole, ModelTier

registry = ModelRegistry.from_yaml("config/models.yaml")
spec = registry.get_for_role(ModelRole.CODER, tier=ModelTier.TIER1_FAST)
response = await gateway_client.complete(spec.name, messages)
```

## Safety Rules

### Sandbox Trust Boundary
- The orchestrator NEVER executes code directly.
- All code execution goes through `SandboxClient` → sandbox worker container.
- The sandbox worker runs as a non-root user with `--cap-drop=ALL` and
  `--read-only`, with network access disabled.

### Command & Path Allowlists
- Only commands in `config/security.yaml:allowed_commands` may be submitted.
- File access must stay within `config/security.yaml:allowed_paths`.
- Enforce with `CommandPolicy.assert_allowed()` and `PathPolicy.assert_allowed()`.

### Prompt Injection
- Strip system-role overrides from user-supplied content before passing to models.
- Set `max_user_content_length` per `config/security.yaml`.

### Secrets
- Never log API keys, tokens, passwords, or credentials.
- Call `redact_dict()` / `redact_string()` before any structured logging.
- `ObservabilityEvent.metadata` is auto-redacted by the `field_validator`.

### Destructive Actions
- Actions listed in `config/security.yaml:destructive_actions_require_approval`
  must go through `ApprovalPolicy` and pause for human confirmation.

## Required Checks (CI must pass before merge)

1. `make fmt-check` – Ruff format check
2. `make lint` – Ruff lint
3. `make typecheck` – strict Mypy
4. `make test-unit` – unit tests (no LLMs)
5. `make test-graph` – graph routing tests (fake clients only)

Model-dependent evaluations run via `make evals` and are **never** blocking CI.

## Coding Conventions

- Full type annotations on all public functions.
- `pydantic.BaseModel` for all data contracts.
- Persisted schemas include `schema_version: int = Field(default=1, ge=1)`.
- Bump `schema_version` on every backward-incompatible change.
- `pytest` markers: `unit`, `graph`, `integration`, `e2e`, `llm`.
  Tests marked `llm` must NEVER run in normal CI.
- Use `structlog` for structured logging.
- Observability events conform to `contracts.events.ObservabilityEvent`.

## Versioned Artifacts

Bump version/schema whenever making backward-incompatible changes to:

| Artifact | Version field |
|----------|--------------|
| `AgentState` subclasses | `schema_version` field |
| `ObservabilityEvent` | `schema_version` field |
| `config/models.yaml` | `schema_version:` top-level key |
| `config/routing.yaml` | `schema_version:` top-level key |
| Prompts in `prompts/` | `<!-- version: N -->` comment header |
| Eval datasets in `evals/datasets/` | `{"schema_version": N}` first line |

## Recommended Next Implementation Issue

After this foundation is merged, the recommended next issue is:

> **Implement core graph wiring**: Connect the main orchestrator graph with
> all nodes (intake → assessment → context → planning → implementation →
> review → verification → finalization), wire conditional edges for tier
> escalation and retry loops, and integrate fake model clients in the
> graph-test suite.
