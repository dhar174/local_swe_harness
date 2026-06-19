"""Sensitive value redaction utilities."""
from __future__ import annotations

import re
from typing import Any

_SENSITIVE_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password|credential)[^=]*=[^\s]+"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*"),
    re.compile(r"(?i)sk-[A-Za-z0-9]{20,}"),
]

_REPLACEMENT = "<redacted>"


def redact_string(text: str) -> str:
    """Replace recognized sensitive patterns in *text* with ``<redacted>``."""
    for pattern in _SENSITIVE_PATTERNS:
        text = pattern.sub(_REPLACEMENT, text)
    return text


def redact_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Recursively redact sensitive values in a dictionary."""
    sensitive_keys = {"api_key", "token", "secret", "password", "credential", "auth"}
    out: dict[str, Any] = {}
    for k, v in data.items():
        if k.lower() in sensitive_keys:
            out[k] = _REPLACEMENT
        elif isinstance(v, dict):
            out[k] = redact_dict(v)
        elif isinstance(v, str):
            out[k] = redact_string(v)
        else:
            out[k] = v
    return out
