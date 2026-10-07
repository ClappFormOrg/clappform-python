"""Every documented code snippet actually runs.

The guides pull their fenced code out of ``docs/snippets/*.py`` via the mkdocs
snippets extension, and each of those modules exposes a ``run()`` (or
``build_mock()`` + ``run()``) entry point that exercises the snippet against
``LocalMock``. This test drives every one of them, and every Python block in
the README, so a doc example that stops working fails the suite here as well
as the docs build: the "docs can't rot" guarantee, enforced in CI.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_SNIPPETS_DIR = _ROOT / "docs" / "snippets"
_README = _ROOT / "README.md"


@pytest.fixture(autouse=True)
def _no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail any snippet that would open a real gRPC channel.

    Several blocks construct a client without ``transport=`` because that is
    what readers write. Constructing one opens nothing; a call would, so a block
    that reaches the network by mistake fails here instead of hanging CI.
    """
    import grpc

    def _refuse(*_args, **_kwargs):
        raise AssertionError("a docs snippet tried to open a network channel")

    monkeypatch.setattr(grpc, "secure_channel", _refuse)
    monkeypatch.setattr(grpc, "insecure_channel", _refuse)


def _load(name: str):
    """Import a snippet module by file path (docs/snippets is not on sys.path)."""
    path = _SNIPPETS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"docs_snippets_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _stub_discovery(monkeypatch: pytest.MonkeyPatch, cluster: str = "") -> None:
    """Answer DNS discovery for blocks that construct location-only clients.

    CI has no such DNS record, so the resolver is stubbed; the snippets
    themselves stay clean and reader-facing.
    """
    from clappform import _discovery

    monkeypatch.setattr(_discovery, "discover_cluster", lambda location: cluster)


def _inject_transport(monkeypatch: pytest.MonkeyPatch, transport) -> None:
    """Make ``from clappform import Clappform`` build clients on ``transport``.

    For blocks written against a real cluster: every client they construct
    without ``transport=`` gets the mock instead, so their calls run.
    """
    import clappform

    real = clappform.Clappform

    class _OnMock(real):  # type: ignore[misc, valid-type]
        def __init__(self, *args, **kwargs):
            kwargs.setdefault("transport", transport)
            super().__init__(*args, **kwargs)

    monkeypatch.setattr(clappform, "Clappform", _OnMock)


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
        "migrating",
        "cookbook",
        "actionflow_scripts",
        "troubleshooting",
        "performance",
        "lifecycle",
        "security",
        "calling_convention",
    } <= found


def test_quickstart_snippet_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    # The index block connects location-only and reads; it runs on the mock.
    module = _load("quickstart")
    mock = module.build_mock()
    _stub_discovery(monkeypatch)
    _inject_transport(monkeypatch, mock)
    module.run(mock)


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


def test_errors_and_retries_snippet_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    _stub_discovery(monkeypatch)
    module = _load("errors_and_retries")
    module.run(module.build_mock())


def test_testing_snippet_runs() -> None:
    module = _load("testing")
    module.run()


def test_migrating_snippet_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    _stub_discovery(monkeypatch)
    module = _load("migrating")
    module.run(module.build_mock())


def test_cookbook_snippet_runs() -> None:
    module = _load("cookbook")
    module.run(module.build_mock(), module.build_second_cluster_mock())


def test_actionflow_scripts_snippet_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    _stub_discovery(monkeypatch)
    module = _load("actionflow_scripts")
    module.run(module.build_mock())


def test_lifecycle_snippet_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    # One location discovers onto another cluster, so the snippet shows a clone
    # that owns its own connections.
    from clappform import _discovery

    clusters = {"acme": "", "noord-brabant": "prod-lts"}
    monkeypatch.setattr(_discovery, "discover_cluster", lambda location: clusters[location])
    module = _load("lifecycle")
    module.run()


def test_security_snippet_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    _stub_discovery(monkeypatch)
    monkeypatch.setenv("CLAPPFORM_API_KEY", "cf_live_test")
    module = _load("security")
    module.run(module.build_mock())


def test_calling_convention_snippet_runs() -> None:
    module = _load("calling_convention")
    module.run(module.build_mock())


def test_troubleshooting_snippet_runs() -> None:
    module = _load("troubleshooting")
    module.run(module.build_mock())


def test_performance_snippet_runs() -> None:
    module = _load("performance")
    module.run(module.build_mock())


@pytest.mark.parametrize(
    "name",
    [
        "quickstart",
        "dataframes",
        "client_operations",
        "multi_cluster",
        "migrating",
        "cookbook",
        "actionflow_scripts",
        "lifecycle",
        "security",
        "calling_convention",
    ],
)
def test_snippet_modules_import_clean(name: str) -> None:
    """Importing a snippet module must have no side effects (no top-level run)."""
    module = _load(name)
    assert hasattr(module, "run")


# -- README ------------------------------------------------------------------


def _readme_text() -> str:
    return _README.read_text(encoding="utf-8")


def _readme_python_blocks() -> list[str]:
    return re.findall(r"^```python\n(.*?)^```", _readme_text(), flags=re.MULTILINE | re.DOTALL)


def _readme_mock():
    """The data the README's real-cluster blocks read and write."""
    from clappform.testing import LocalMock

    mock = LocalMock()
    mock.seed_collection_slug("sales_orders", id="sales_orders-id")
    mock.seed(
        "sales_orders-id",
        [
            {"order_id": "A-1", "amount": 100.0, "status": "open"},
            {"order_id": "A-2", "amount": 50.0, "status": "closed"},
        ],
    )
    return mock


def test_readme_has_python_blocks() -> None:
    assert len(_readme_python_blocks()) >= 2


@pytest.mark.parametrize("index", range(len(_readme_python_blocks())))
def test_readme_block_runs(index: int, monkeypatch: pytest.MonkeyPatch) -> None:
    """Compile and run each README block.

    A block that builds its own ``LocalMock`` runs as written. A block written
    against a real cluster runs with a seeded mock injected as the transport and
    DNS discovery stubbed, so its calls and attribute names are checked against
    the client without a network.
    """
    source = _readme_python_blocks()[index]
    code = compile(source, f"README.md python block {index}", "exec")
    if "LocalMock" not in source:
        _stub_discovery(monkeypatch)
        _inject_transport(monkeypatch, _readme_mock())
    exec(code, {"__name__": f"readme_block_{index}"})  # noqa: S102 -- the README is ours


def _client_surface() -> set[str]:
    """Every public name reachable on a client, its families, services and handles."""
    from clappform import Clappform, CollectionHandle, QueryHandle, ReadResult
    from clappform.testing import LocalMock

    cf = Clappform(location="acme", api_key="test", transport=LocalMock())
    names = {n for n in dir(cf) if not n.startswith("_")}
    for family in ("data", "client", "auth", "notifier"):
        api = getattr(cf, family)
        for service_name in (n for n in vars(api) if not n.startswith("_")):
            names.add(service_name)
            service = getattr(api, service_name)
            names.update(n for n in dir(service) if not n.startswith("_"))
    for cls in (CollectionHandle, QueryHandle, ReadResult, LocalMock):
        names.update(n for n in dir(cls) if not n.startswith("_"))
    return names


def test_readme_inline_calls_exist() -> None:
    """Method names in the README's prose and tables exist on the client."""
    prose = re.sub(r"^```.*?^```", "", _readme_text(), flags=re.MULTILINE | re.DOTALL)
    called = set()
    for span in re.findall(r"`([^`]+)`", prose):
        called.update(re.findall(r"\.(\w+)\(", span))
    called -= {"drop"}  # pandas, not the client
    missing = sorted(called - _client_surface())
    assert not missing, f"README calls names the client does not have: {missing}"
