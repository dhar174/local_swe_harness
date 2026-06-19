"""Unit tests for security policy modules."""
from __future__ import annotations

import pytest

from swe_agents.security.command_policy import CommandPolicy
from swe_agents.security.path_policy import PathPolicy
from swe_agents.security.redaction import redact_dict, redact_string
from swe_agents.security.approval_policy import ApprovalAction, requires_approval


pytestmark = pytest.mark.unit


class TestCommandPolicy:
    def test_allowed_command(self) -> None:
        policy = CommandPolicy(["pytest", "ruff check"])
        assert policy.is_allowed(["pytest", "--tb=short"])

    def test_denied_command(self) -> None:
        policy = CommandPolicy(["pytest"])
        assert not policy.is_allowed(["rm", "-rf", "/"])

    def test_assert_allowed_raises_on_denied(self) -> None:
        policy = CommandPolicy(["pytest"])
        with pytest.raises(PermissionError):
            policy.assert_allowed(["curl", "http://evil.com"])


class TestPathPolicy:
    def test_allowed_path(self, tmp_path: pytest.TempPathFactory) -> None:
        policy = PathPolicy([str(tmp_path)])
        assert policy.is_allowed(tmp_path / "subdir" / "file.py")

    def test_denied_path(self, tmp_path: pytest.TempPathFactory) -> None:
        policy = PathPolicy([str(tmp_path)])
        assert not policy.is_allowed("/etc/passwd")


class TestRedaction:
    def test_redact_api_key_in_string(self) -> None:
        text = "api_key=sk-supersecret123456789abcdef"
        assert "sk-supersecret" not in redact_string(text)

    def test_redact_sensitive_dict_key(self) -> None:
        result = redact_dict({"api_key": "real-key", "user": "alice"})
        assert result["api_key"] == "<redacted>"
        assert result["user"] == "alice"

    def test_redact_nested_dict(self) -> None:
        result = redact_dict({"outer": {"token": "abc"}})
        assert result["outer"]["token"] == "<redacted>"


class TestApprovalPolicy:
    def test_force_push_requires_approval(self) -> None:
        assert requires_approval(ApprovalAction.FORCE_PUSH)

    def test_delete_branch_no_approval(self) -> None:
        assert not requires_approval(ApprovalAction.DELETE_BRANCH)
