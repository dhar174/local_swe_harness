# Architecture Overview

See `AGENTS.md` for the canonical reference. This document provides
additional context for the system design decisions.

## Tier Model

The system uses a three-tier model selection strategy:

1. **Tier 1 – Fast Local**: Small quantized models (7B class) running via
   llama.cpp or Ollama. Used for simple, well-scoped tasks.
2. **Tier 2 – Heavy Local**: Large quantized models (32B+ class). Used for
   complex refactors, large context, or after tier-1 failures.
3. **Tier 3 – Cloud**: Commercial APIs (Anthropic Claude, OpenAI GPT-4).
   Reserved for ambiguous, high-risk, or repeatedly failing tasks.

## Graph Design

The main orchestrator graph follows a linear pipeline with conditional edges:

```
intake → assessment → context → planning → implementation
    → review → verification → finalization
```

Conditional edges implement:
- Tier escalation (based on complexity score or retry count)
- Retry loops (implementation → review on rejection)
- Human approval gates (before destructive actions)
- Interrupt/resume (for checkpoint-based state recovery)

## Configuration-Driven Model Assignment

Model assignments are never hardcoded. The `ModelRegistry` class loads
from `config/models.yaml` and resolves models by role and tier at runtime.
This allows model swaps without code changes.

## Related Documents

- `AGENTS.md` – Safety rules and coding conventions
- `docs/model-roles.md` – Detailed model role descriptions
- `docs/routing-policy.md` – Routing algorithm documentation
- `docs/sandbox-security.md` – Sandbox security design
- `docs/adr/` – Architecture Decision Records
