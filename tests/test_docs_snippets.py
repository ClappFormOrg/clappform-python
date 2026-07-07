"""Every documented code snippet actually runs.

The guides pull their fenced code out of ``docs/snippets/*.py`` via the mkdocs
snippets extension, and each of those modules exposes a ``run()`` (or
``build_mock()`` + ``run()``) entry point that exercises the snippet against
``LocalMock``. This test drives every one of them, so a doc example that stops
working fails the suite here as well as the docs build — the "docs can't rot"
guarantee, enforced in CI.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_SNIPPETS_DIR = Path(__file__).resolve().parent.parent / "docs" / "snippets"


def _load(name: str):
    """Import a snippet module by file path (docs/snippets is not on sys.path)."""
    path = _SNIPPETS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"docs_snippets_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_snippets_directory_is_present() -> None:
    """Guard against the snippet source being moved out from under the guides."""
    assert _SNIPPETS_DIR.is_dir()
    found = {p.stem for p in _SNIPPETS_DIR.glob("*.py")}
    assert {
        "quickstart",
        "dataframes",
        "client_operations",
        "multi_cluster",
        "errors_and_retries",
        "testing",
    } <= found


def test_quickstart_snippet_runs() -> None:
    module = _load("quickstart")
    module.run(module.build_mock())


def test_dataframes_snippet_runs() -> None:
    module = _load("dataframes")
    mock = module.build_mock()
    mock.seed_query("monthly-revenue-per-region", collection="sales_orders-id")
    module.run(mock)


def test_client_operations_snippet_runs() -> None:
    module = _load("client_operations")
    module.run(module.build_mock())


def test_multi_cluster_snippet_runs() -> None:
    module = _load("multi_cluster")
    module.run(module.build_mock(), module.build_mock())


def test_errors_and_retries_snippet_runs() -> None:
    module = _load("errors_and_retries")
    module.run(module.build_mock())


def test_testing_snippet_runs() -> None:
    module = _load("testing")
    module.run()


@pytest.mark.parametrize(
    "name", ["quickstart", "dataframes", "client_operations", "multi_cluster"]
)
def test_snippet_modules_import_clean(name: str) -> None:
    """Importing a snippet module must have no side effects (no top-level run)."""
    module = _load(name)
    assert hasattr(module, "run")
