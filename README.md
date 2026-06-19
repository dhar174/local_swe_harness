# tiered-swe-agents

> A LangGraph multi-agent SWE system that routes coding tasks across fast
> local, heavy local, and cloud tiers. Specialized agents plan, inspect
> repositories, write and review code, run tests, recover from failures,
> and escalate only when complexity, risk, or repeated failures require
> stronger models.

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Docker & Docker Compose (optional, for the full dev stack)

### Install

```bash
git clone https://github.com/dhar174/local_swe_harness.git
cd local_swe_harness
uv sync --all-packages --all-extras
make pre-commit-install
cp .env.example .env
```

### Run Quality Checks

```bash
make ci            # fmt + lint + typecheck + unit tests + coverage
make test-unit     # unit tests only
make test-graph    # graph routing tests (fake models, no LLMs)
make evals         # evaluation harness (fake models only)
```

### Start the Development Stack

```bash
make docker-up     # starts orchestrator, model-gateway, sandbox-worker, postgres
make docker-logs   # tail logs
make docker-down   # stop
```

### Minimal End-to-End Example (fake models)

```python
from contracts.state import Tier
from contracts.tasks import Task, TaskRequest
from model_clients.fake import FakeModelClient
from model_clients.capabilities import ModelRole, ModelTier, ModelSpec, ModelCapability
from model_clients.registry import ModelRegistry
from swe_agents.routing.escalation import should_escalate, next_tier
from swe_agents.state import OrchestratorState

# 1. Build a fake registry (production: load from config/models.yaml)
specs = [
    ModelSpec(name="fake-coder", tier=ModelTier.TIER1_FAST,
              roles=[ModelRole.CODER], capabilities=[ModelCapability.CHAT]),
]
registry = ModelRegistry(specs)

# 2. Create initial state
state = OrchestratorState(
    task_id="demo-001",
    thread_id="th-001",
    tier=Tier.TIER1_FAST,
    complexity_score=0.3,
)

# 3. Check routing decision
if should_escalate(state):
    state.tier = next_tier(state.tier)
    print(f"Escalated to {state.tier}")
else:
    print(f"Running on {state.tier}")

# 4. Resolve model from registry (config-driven, not hardcoded)
spec = registry.get_for_role(ModelRole.CODER)
print(f"Using model: {spec.name}")

# 5. Call fake model client (swap with GatewayModelClient for real inference)
import asyncio
client = FakeModelClient(responses=["Fix applied."])
resp = asyncio.run(client.complete(spec.name, [{"role": "user", "content": "Fix the bug"}]))
print(resp["choices"][0]["message"]["content"])
# → Fix applied.
```

See `tests/end_to_end/test_fake_e2e.py` for a runnable version.

## Architecture

See [`AGENTS.md`](AGENTS.md) for architecture boundaries, safety rules,
required checks, and coding conventions.

```
packages/contracts/      Shared typed schemas
packages/model_clients/  Capability registry + fake clients
packages/tool_clients/   Sandbox / repo / search interfaces
apps/orchestrator/       LangGraph graphs, nodes, agents, routing
services/model_gateway/  Backend adapters (llama.cpp, Ollama, cloud)
services/sandbox_worker/ Sandboxed code execution
services/repo_indexer/   Symbol + dependency indexing
config/                  YAML configuration (models, routing, security)
evals/                   Evaluation harness and datasets
```

## GitHub Settings

See [`docs/github-settings-checklist.md`](docs/github-settings-checklist.md)
for required repository configuration and a helper script.

## License

MIT – see [`LICENSE`](LICENSE).
