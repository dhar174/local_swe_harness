"""Architecture tests enforcing module dependency directions.

Rules:
- contracts  → no internal imports (pure data)
- model_clients → may import contracts only
- tool_clients  → may import contracts only
- swe_agents    → may import contracts, model_clients, tool_clients
- services      → may NOT import swe_agents
"""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

import pytest

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).parent.parent


def iter_python_files(directory: Path) -> Iterator[Path]:
    yield from directory.rglob("*.py")


def get_top_level_imports(path: Path) -> set[str]:
    """Return set of top-level module names imported by a Python file."""
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError:
        return set()
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    return imports


def test_contracts_has_no_internal_imports() -> None:
    """contracts package must not import other internal packages."""
    internal = {"swe_agents", "model_clients", "tool_clients",
                "model_gateway", "sandbox_worker", "repo_indexer"}
    contracts_src = REPO_ROOT / "packages" / "contracts" / "src"
    violations = []
    for pyfile in iter_python_files(contracts_src):
        imported = get_top_level_imports(pyfile)
        bad = imported & internal
        if bad:
            violations.append(f"{pyfile.relative_to(REPO_ROOT)}: imports {bad}")
    assert not violations, "\n".join(violations)


def test_model_clients_only_imports_contracts() -> None:
    """model_clients may only import contracts from internal packages."""
    forbidden = {"swe_agents", "tool_clients", "model_gateway",
                 "sandbox_worker", "repo_indexer"}
    src = REPO_ROOT / "packages" / "model_clients" / "src"
    violations = []
    for pyfile in iter_python_files(src):
        imported = get_top_level_imports(pyfile)
        bad = imported & forbidden
        if bad:
            violations.append(f"{pyfile.relative_to(REPO_ROOT)}: imports {bad}")
    assert not violations, "\n".join(violations)


def test_tool_clients_only_imports_contracts() -> None:
    """tool_clients may only import contracts from internal packages."""
    forbidden = {"swe_agents", "model_clients", "model_gateway",
                 "sandbox_worker", "repo_indexer"}
    src = REPO_ROOT / "packages" / "tool_clients" / "src"
    violations = []
    for pyfile in iter_python_files(src):
        imported = get_top_level_imports(pyfile)
        bad = imported & forbidden
        if bad:
            violations.append(f"{pyfile.relative_to(REPO_ROOT)}: imports {bad}")
    assert not violations, "\n".join(violations)


def test_services_do_not_import_swe_agents() -> None:
    """Service packages must not depend on the orchestrator application."""
    services_src = REPO_ROOT / "services"
    violations = []
    for pyfile in iter_python_files(services_src):
        imported = get_top_level_imports(pyfile)
        if "swe_agents" in imported:
            violations.append(str(pyfile.relative_to(REPO_ROOT)))
    assert not violations, f"Services import swe_agents: {violations}"
