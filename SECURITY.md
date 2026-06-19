# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| main    | ✅        |
| < 0.1.0 | ❌        |

## Reporting a Vulnerability

Please **do not** open a public issue for security vulnerabilities.

Report vulnerabilities privately via
[GitHub Security Advisories](https://github.com/dhar174/local_swe_harness/security/advisories/new).

You will receive a response within 48 hours acknowledging receipt.
We aim to release a fix within 7 days for critical vulnerabilities.

## Sandbox Trust Boundary

The system executes code only inside the sandboxed `sandbox-worker` container:

- Runs as non-root (`sandbox` user)
- All Linux capabilities dropped (`--cap-drop=ALL`)
- Read-only root filesystem (`--read-only`)
- Network access disabled (`SANDBOX_NETWORK_ACCESS=false`)
- Strict CPU and memory limits
- Commands and paths restricted to explicit allowlists

**The orchestrator NEVER executes arbitrary code directly.**

## Secrets Handling

- API keys and tokens are never logged or emitted in observability events.
- `redact_dict()` / `redact_string()` must be called before any logging.
- `ObservabilityEvent.metadata` is auto-redacted.
- `.env` files are gitignored. Use `.env.example` as a template only.

## Supply Chain Security

- Dependencies are pinned in `uv.lock`.
- Dependabot monitors all Python packages, GitHub Actions, and Docker images.
- CodeQL and Gitleaks scan every pull request.
- Container images use minimal `python:3.12-slim` base.
