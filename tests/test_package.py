"""Package-level sanity: metadata, versioning, and import surface."""

import re
from importlib.metadata import metadata, version

from packaging.version import Version

import clappform


def test_version_is_pep440() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+([ab]|rc)?\d*", clappform.__version__)
    assert clappform.__version__.startswith("6.")


def test_version_matches_packaged_version() -> None:
    """`__version__` is what hatchling packaged, so the two can never drift.

    hatchling reads the literal in ``clappform/__init__.py`` for the
    distribution version, and this asserts the built metadata agrees. A release
    that bumps one and not the other fails here instead of shipping a wheel
    whose ``repr(client)`` reports the previous version.
    """
    assert clappform.__version__ == version("clappform")


def test_proto_version_matches_pin() -> None:
    from pathlib import Path

    pin = Path(__file__).parent.parent / "COMMONS_VERSION"
    assert clappform.__proto_version__ == pin.read_text().strip()


def test_dataframe_libraries_are_extras_not_core_deps() -> None:
    meta = metadata("clappform")
    requires = [r for r in meta.get_all("Requires-Dist") or [] if "extra" not in r]
    joined = " ".join(requires).lower()
    assert "grpcio" in joined
    assert "protobuf" in joined
    for lib in ("pandas", "polars", "pyarrow"):
        assert lib not in joined, f"{lib} must be an extra, not a core dependency"


def test_generated_surface_imports() -> None:
    from clappform.gen.clappform.data.v1.insert import insert_pb2
    from clappform.services import API_FAMILIES

    assert set(API_FAMILIES) == {"auth", "client", "data", "notifier"}
    request = insert_pb2.InsertRequest(collection="orders")
    assert request.collection == "orders"


def test_nbflow_is_excluded() -> None:
    from pathlib import Path

    gen = Path(clappform.__file__).parent / "gen" / "clappform"
    assert not (gen / "nbflow").exists()


def _floor(requirement: str) -> Version:
    import re

    match = re.search(r">=([\d.]+)", requirement)
    assert match, requirement
    return Version(match.group(1))


def _stamps(pattern: str) -> set[Version]:
    import re
    from pathlib import Path

    gen = Path(clappform.__file__).parent / "gen"
    found = set()
    for path in gen.rglob("*.py"):
        match = re.search(pattern, path.read_text(encoding="utf-8"))
        if match:
            found.add(Version(match.group(1)))
    assert found, pattern
    return found


def _requirement(name: str) -> str:
    from importlib.metadata import requires

    return next(r for r in requires("clappform") or [] if r.startswith(name) and "extra" not in r)


def test_grpcio_floor_covers_generated_stubs() -> None:
    # Every *_pb2_grpc.py refuses to import on a grpcio older than the one that
    # generated it, so the declared floor must be at least the newest stamp.
    newest = max(_stamps(r"GRPC_GENERATED_VERSION = '([\d.]+)'"))
    assert _floor(_requirement("grpcio")) >= newest


def test_protobuf_floor_covers_generated_messages() -> None:
    # Regenerating with a newer grpcio-tools stamps newer gencode; the protobuf
    # floor has to move with it or older runtimes fail at import.
    newest = max(_stamps(r"# Protobuf Python Version: ([\d.]+)"))
    assert _floor(_requirement("protobuf")) >= newest
