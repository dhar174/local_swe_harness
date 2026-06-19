#!/usr/bin/env bash
# configure_github.sh – Apply recommended GitHub repository settings.
#
# Usage:
#   scripts/configure_github.sh --dry-run         (preview, no changes)
#   scripts/configure_github.sh --branch-protection
#   scripts/configure_github.sh --labels
#   scripts/configure_github.sh --all
#
# Requires: gh (GitHub CLI) authenticated with repo admin rights.

set -euo pipefail

REPO="${GITHUB_REPOSITORY:-dhar174/local_swe_harness}"
DRY_RUN=false

log() { echo "[configure_github] $*"; }
dry() { if $DRY_RUN; then log "[DRY-RUN] $*"; else eval "$*"; fi; }

for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=true ;;
    --branch-protection) ACTION=branch_protection ;;
    --labels) ACTION=labels ;;
    --all) ACTION=all ;;
  esac
done

branch_protection() {
  log "Applying branch protection to main..."
  dry gh api \
    --method PUT \
    -H "Accept: application/vnd.github+json" \
    "/repos/${REPO}/branches/main/protection" \
    -f required_status_checks='{"strict":true,"contexts":["quality","test-unit","test-graph","test-architecture","CodeQL"]}' \
    -f enforce_admins=true \
    -f required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":true}' \
    -f restrictions=null \
    -f allow_force_pushes=false \
    -f allow_deletions=false \
    -f required_linear_history=true
}

create_labels() {
  log "Creating labels..."
  labels=(
    "bug|d73a4a|Something isn't working"
    "enhancement|a2eeef|New feature or request"
    "security|e4e669|Security-related change"
    "orchestrator|0075ca|Orchestrator app"
    "model-gateway|cfd3d7|Model gateway service"
    "sandbox-worker|e4e669|Sandbox worker service"
    "contracts|bfd4f2|Shared data contracts"
    "routing|d4c5f9|Routing logic"
    "evaluations|f9d0c4|Eval harness"
    "ci|0e8a16|CI/CD changes"
    "documentation|0075ca|Documentation"
    "needs-triage|e4e669|Needs attention"
    "dependencies|0366d6|Dependency updates"
  )
  for entry in "${labels[@]}"; do
    IFS='|' read -r name color description <<< "$entry"
    dry gh label create "$name" --color "$color" --description "$description" \
      --repo "$REPO" 2>/dev/null || \
    dry gh label edit "$name" --color "$color" --description "$description" \
      --repo "$REPO"
  done
}

case "${ACTION:-}" in
  branch_protection) branch_protection ;;
  labels) create_labels ;;
  all)
    branch_protection
    create_labels
    ;;
  *)
    log "No action specified. Use --dry-run --all to preview all changes."
    log "See docs/github-settings-checklist.md for manual configuration steps."
    ;;
esac

log "Done."
