# ADR 0003: Sandboxed Code Execution

## Status: Accepted

## Context

An SWE agent needs to execute code (tests, lint, type checks) in the context
of a repository. Executing this code in the orchestrator process is unsafe.

## Decision

All code execution is performed by the `sandbox_worker` service:
- Separate Docker container with non-root user
- `--cap-drop=ALL`, `--read-only`, `--network=none`
- Strict CPU and memory limits
- Command and path allowlists enforced server-side

## Consequences

- Sandbox isolation limits blast radius of malicious or buggy generated code
- Adds operational complexity (extra container, IPC overhead)
