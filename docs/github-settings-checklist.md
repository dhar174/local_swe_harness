# GitHub Repository Settings Checklist

Run `scripts/configure_github.sh --dry-run` first to preview all changes.

## Branch Protection (main)

- [ ] Require pull request before merging
  - [ ] Required approvals: **1** (increase to 2 after team grows)
  - [ ] Dismiss stale pull request approvals when new commits are pushed
  - [ ] Require review from CODEOWNERS
- [ ] Require status checks to pass before merging
  - [ ] Required checks:
    - `quality` (Lint, Format & Type Check)
    - `test-unit` (Unit Tests)
    - `test-graph` (Graph Routing Tests)
    - `test-architecture` (Architecture Tests)
    - `CodeQL` (from security.yml)
- [ ] Require branches to be up to date before merging
- [ ] Require linear history (squash or rebase merge only)
- [ ] Include administrators

## Actions Permissions

- [ ] Allow all actions and reusable workflows
- [ ] Allow GitHub Actions to create and approve pull requests: **disabled**
- [ ] Workflow permissions: Read repository contents and packages

## Secret Scanning

- [ ] Enable secret scanning
- [ ] Enable push protection (block pushes containing secrets)

## Dependabot

- [ ] Enable Dependabot security updates
- [ ] Enable Dependabot version updates (configured in `.github/dependabot.yml`)

## Protected Environments

- [ ] Create `evaluation` environment
  - Required reviewers: @dhar174
  - Deployment branches: `main` only

## Code Security

- [ ] Enable CodeQL analysis (configured in `.github/workflows/security.yml`)

## Labels (create if missing)

Run: `scripts/configure_github.sh --labels`

| Label | Color | Description |
|-------|-------|-------------|
| `bug` | `d73a4a` | Something isn't working |
| `enhancement` | `a2eeef` | New feature or request |
| `security` | `e4e669` | Security-related change |
| `orchestrator` | `0075ca` | Orchestrator app |
| `model-gateway` | `cfd3d7` | Model gateway service |
| `sandbox-worker` | `e4e669` | Sandbox worker service |
| `contracts` | `bfd4f2` | Shared data contracts |
| `routing` | `d4c5f9` | Routing logic |
| `evaluations` | `f9d0c4` | Eval harness |
| `ci` | `0e8a16` | CI/CD changes |
| `documentation` | `0075ca` | Documentation |
| `needs-triage` | `e4e669` | Needs attention |
| `dependencies` | `0366d6` | Dependency updates |

## Notifications

All items above that remain unchecked require **manual configuration** in the
GitHub web UI or via the GitHub CLI / API.

See also: `scripts/configure_github.sh` for automatable steps.
