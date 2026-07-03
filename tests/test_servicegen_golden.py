"""Golden-file tests for the service-layer generator.

Fixture protos are compiled to a FileDescriptorSet at test time, run through
servicegen, and the emitted sources are compared byte-for-byte against the
checked-in golden files. Any intentional generator change must update the
goldens: run ``UPDATE_GOLDEN=1 python -m pytest tests/test_servicegen_golden.py``.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).parent.parent / "tools"
FIXTURES = Path(__file__).parent / "servicegen_fixtures"
GOLDEN = Path(__file__).parent / "servicegen_golden"

sys.path.insert(0, str(TOOLS))
import servicegen  # noqa: E402


@pytest.fixture(scope="module")
def descriptor_set(tmp_path_factory: pytest.TempPathFactory) -> bytes:
    out = tmp_path_factory.mktemp("descriptors") / "fixtures.binpb"
    protos = [p.relative_to(FIXTURES).as_posix() for p in sorted(FIXTURES.rglob("*.proto"))]
    subprocess.run(
        [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            f"-I{FIXTURES}",
            f"--descriptor_set_out={out}",
            "--include_imports",
            "--include_source_info",
            *protos,
        ],
        check=True,
        cwd=FIXTURES,
    )
    return out.read_bytes()


def test_generated_sources_match_golden(descriptor_set: bytes) -> None:
    sources = servicegen.generate_sources(descriptor_set)

    if os.environ.get("UPDATE_GOLDEN") == "1":
        GOLDEN.mkdir(exist_ok=True)
        for stale in GOLDEN.glob("*.py"):
            stale.unlink()
        for name, source in sources.items():
            (GOLDEN / name).write_text(source, encoding="utf-8", newline="\n")

    golden_files = {p.name for p in GOLDEN.glob("*.py")}
    assert golden_files == set(sources), (
        f"generated module set {sorted(sources)} != golden set {sorted(golden_files)}"
    )
    for name, source in sources.items():
        expected = (GOLDEN / name).read_text(encoding="utf-8")
        assert source == expected, f"{name} drifted from golden — see UPDATE_GOLDEN"


def test_reserved_field_is_not_flattened(descriptor_set: bytes) -> None:
    source = servicegen.generate_sources(descriptor_set)["demo.py"]
    collide = source[source.index("def collide") : source.index("class DemoAPI")]
    assert "location: str | None = None" in collide  # the per-call arg stays
    assert "name collision" in collide  # and the field is documented as skipped
    assert "payload: str | None = None" in collide  # non-colliding fields flatten


def test_pagination_variant_emitted_only_where_applicable(descriptor_set: bytes) -> None:
    source = servicegen.generate_sources(descriptor_set)["demo.py"]
    assert "def iter_get_all(" in source
    assert "def iter_get(" not in source
    assert "def iter_upload(" not in source
