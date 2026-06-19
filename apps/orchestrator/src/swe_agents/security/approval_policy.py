"""Human approval policy for destructive actions."""
from __future__ import annotations

import enum


class ApprovalAction(str, enum.Enum):
    DELETE_BRANCH = "delete_branch"
    FORCE_PUSH = "force_push"
    DROP_TABLE = "drop_table"
    DEPLOY_PRODUCTION = "deploy_production"


_ALWAYS_REQUIRE_APPROVAL: frozenset[ApprovalAction] = frozenset({
    ApprovalAction.FORCE_PUSH,
    ApprovalAction.DROP_TABLE,
    ApprovalAction.DEPLOY_PRODUCTION,
})


def requires_approval(action: ApprovalAction) -> bool:
    return action in _ALWAYS_REQUIRE_APPROVAL
