"""Package-level sanity: metadata, versioning, and import surface."""

import re
from importlib.metadata import metadata, version

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
