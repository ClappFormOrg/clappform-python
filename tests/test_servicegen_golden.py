"""Golden-file tests for the service-layer generator.

Fixture protos are compiled to a FileDescriptorSet at test time, run through
servicegen, and the emitted sources are compared byte-for-byte against the
checked-in golden files. Any intentional generator change must update the
goldens: run ``UPDATE_GOLDEN=1 python -m pytest tests/test_servicegen_golden.py``.

The remaining tests compile small inline protos to cover the cases that stop
generation or that need more than one service per family.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from google.protobuf import descriptor_pb2

TOOLS = Path(__file__).parent.parent / "tools"
FIXTURES = Path(__file__).parent / "servicegen_fixtures"
GOLDEN = Path(__file__).parent / "servicegen_golden"

sys.path.insert(0, str(TOOLS))
import servicegen  # noqa: E402


def compile_protos(out: Path, include: Path, protos: list[str]) -> bytes:
    descriptors = out / "descriptors.binpb"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            f"-I{include}",
            f"-I{FIXTURES}",
            f"--descriptor_set_out={descriptors}",
            "--include_imports",
            "--include_source_info",
            *protos,
        ],
        check=True,
        cwd=include,
    )
    return descriptors.read_bytes()


@pytest.fixture(scope="module")
def descriptor_set(tmp_path_factory: pytest.TempPathFactory) -> bytes:
    out = tmp_path_factory.mktemp("descriptors")
    protos = [p.relative_to(FIXTURES).as_posix() for p in sorted(FIXTURES.rglob("*.proto"))]
    return compile_protos(out, FIXTURES, protos)


@pytest.fixture(scope="module")
def demo_source(descriptor_set: bytes) -> str:
    return servicegen.generate_sources(descriptor_set)["demo.py"]


def method_source(source: str, name: str) -> str:
    start = source.index(f"    def {name}(")
    end = source.find("\n    def ", start + 1)
    return source[start : end if end != -1 else len(source)]


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
        assert source == expected, f"{name} drifted from golden; see UPDATE_GOLDEN"


def test_colliding_fields_get_trailing_underscore(demo_source: str) -> None:
    collide = method_source(demo_source, "collide")
    assert "        location: str | None = None," in collide  # the per-call arg stays
    for param in ("location_: str", "timeout_: int", "from_: str", "payload: str"):
        assert f"        {param} | None = None," in collide
    assert '("location", location_)' in collide
    assert '("timeout", timeout_)' in collide
    assert '("from", from_)' in collide
    assert "name collision" not in collide


def test_keyword_rpc_and_service_names_get_trailing_underscore(demo_source: str) -> None:
    assert "    def import_(" in demo_source
    assert "    def pass_(" in demo_source
    assert "self.global_ = Global(caller)" in demo_source


def test_annotations_and_imports(demo_source: str) -> None:
    imported = method_source(demo_source, "import_")
    thing = "_m_clappform_demo_v1_thing_thing"
    assert f"source: {thing}.Source | int | str | None" in imported
    assert f"state: {thing}.Thing.State | int | str | None" in imported
    assert f"dimensions: {thing}.Thing.Dimensions | Mapping[str, Any] | None" in imported
    # Referenced only as a map value and as a pagination item respectively.
    assert "import clappform.gen.clappform.demo.v1.parts.widget_pb2 as" in demo_source
    assert "import clappform.gen.clappform.demo.v1.parts.gadget_pb2 as" in demo_source


def test_docstring_layout(demo_source: str) -> None:
    imported = method_source(demo_source, "import_")
    assert '"""Import things from an external source.\n\n        The RPC name' in imported
    assert "\n          - relative indentation survives\n" in imported
    assert "\n            state: Initial state of the imported things.\n" in imported
    collide = method_source(demo_source, "collide")
    assert '"""Exercise reserved field names.\n\n        Fields named' in collide


def test_pagination_variant_emitted_only_where_applicable(demo_source: str) -> None:
    assert "def iter_get_all(" in demo_source
    assert "def iter_list_gadgets(" in demo_source
    assert "def iter_get(" not in demo_source
    assert "def iter_upload(" not in demo_source
    bundles = method_source(demo_source, "iter_list_bundles")
    assert "Only ``things`` is yielded; call ``list_bundles`` for ``summaries``." in bundles


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("AzureAuthOAuthACS", "azure_auth_oauth_acs"),
        ("AzureAuthSAMLACS", "azure_auth_saml_acs"),
        ("SendWhatsAppMessage", "send_whatsapp_message"),
        ("DeAuth", "de_auth"),
        ("GetAll", "get_all"),
    ],
)
def test_snake_case(name: str, expected: str) -> None:
    assert servicegen.snake_case(name) == expected


EMPTY = "clappform.v1.commons.Empty"
PING = f"rpc Ping({EMPTY}) returns ({EMPTY});"


def service_proto(package: str, body: str) -> str:
    return (
        'syntax = "proto3";\n'
        f"package {package};\n"
        'import "clappform/v1/commons/commons.proto";\n'
        f"{body}\n"
    )


def write_protos(root: Path, files: dict[str, str]) -> list[str]:
    for name, body in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return sorted(files)


def generate_inline(tmp_path: Path, files: dict[str, str]) -> dict[str, str]:
    protos = write_protos(tmp_path, files)
    return servicegen.generate_sources(compile_protos(tmp_path, tmp_path, protos))


def two_thing_services() -> dict[str, str]:
    service = f"service ThingManagement {{ {PING} }}"
    return {
        f"clappform/demo/v1/{name}/{name}.proto": service_proto(
            f"clappform.demo.v1.{name}", service
        )
        for name in ("alpha", "beta")
    }


def test_colliding_service_names_are_all_suffixed(tmp_path: Path) -> None:
    demo = generate_inline(tmp_path, two_thing_services())["demo.py"]
    assert "class ThingManagementAlpha(" in demo
    assert "class ThingManagementBeta(" in demo
    assert "self.thing_alpha = ThingManagementAlpha(caller)" in demo
    assert "self.thing_beta = ThingManagementBeta(caller)" in demo


def test_output_does_not_depend_on_descriptor_order(tmp_path: Path) -> None:
    protos = write_protos(tmp_path, two_thing_services())
    fds = descriptor_pb2.FileDescriptorSet.FromString(compile_protos(tmp_path, tmp_path, protos))
    reordered = descriptor_pb2.FileDescriptorSet(file=list(reversed(fds.file)))
    assert servicegen.generate_sources(fds.SerializeToString()) == servicegen.generate_sources(
        reordered.SerializeToString()
    )


@pytest.mark.parametrize(
    ("body", "message"),
    [
        (
            f"service S {{ rpc GetUrl({EMPTY}) returns ({EMPTY}); "
            f"rpc GetURL({EMPTY}) returns ({EMPTY}); }}",
            "method get_url",
        ),
        (
            "service S { rpc GetAll(clappform.v1.commons.PaginationRequest) returns (Page); "
            f"rpc IterGetAll({EMPTY}) returns ({EMPTY}); }}\n"
            "message Page { repeated Page items = 1; "
            "clappform.v1.commons.Pagination pagination = 2; }",
            "method iter_get_all",
        ),
        (
            f"service S {{ rpc Set(R) returns ({EMPTY}); }}\n"
            "message R { option deprecated_legacy_json_field_conflicts = true; "
            "int32 timeout = 1; int32 timeout_ = 2; }",
            "keyword argument: timeout_",
        ),
        (
            f"service Thing {{ {PING} }}\nservice ThingManagement {{ {PING} }}",
            "attribute thing",
        ),
    ],
)
def test_ambiguous_names_stop_generation(tmp_path: Path, body: str, message: str) -> None:
    proto = {"clappform/demo/v1/x/x.proto": service_proto("clappform.demo.v1.x", body)}
    with pytest.raises(SystemExit, match=message):
        generate_inline(tmp_path, proto)


@pytest.mark.parametrize("service", ["CollectionManagement", "Query"])
def test_data_family_reserves_handwritten_attributes(tmp_path: Path, service: str) -> None:
    body = f"service {service} {{ {PING} }}"
    proto = {"clappform/data/v1/x/x.proto": service_proto("clappform.data.v1.x", body)}
    with pytest.raises(SystemExit, match="reserved"):
        generate_inline(tmp_path, proto)


def test_underscore_family_gets_camel_case_class(tmp_path: Path) -> None:
    body = f"service PingManagement {{ {PING} }}"
    package = "clappform.data_connector.v1.x"
    proto = {"clappform/data_connector/v1/x/x.proto": service_proto(package, body)}
    sources = generate_inline(tmp_path, proto)
    assert "class DataConnectorAPI:" in sources["data_connector.py"]
