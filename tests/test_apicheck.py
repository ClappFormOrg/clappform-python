"""The proto pass of tools/apicheck.py: removed messages and fields in clappform.gen."""

import sys
from pathlib import Path

from google.protobuf import descriptor_pb2

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
import apicheck  # noqa: E402

PB2 = "src/clappform/gen/clappform/data/v1/export/export_pb2.py"
MODULE = "clappform.gen.clappform.data.v1.export.export_pb2"


def pb2_source(file: descriptor_pb2.FileDescriptorProto) -> str:
    serialized = file.SerializeToString()
    return f"DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile({serialized!r})\n"


def current() -> descriptor_pb2.FileDescriptorProto:
    source = (Path(__file__).parent.parent / PB2).read_text(encoding="utf-8")
    data = apicheck.serialized_descriptor(source)
    assert data is not None
    return descriptor_pb2.FileDescriptorProto.FromString(data)


def test_unchanged_descriptor_reports_nothing() -> None:
    sources = {PB2: pb2_source(current())}
    fields = apicheck.message_fields(sources, "src")
    assert f"{MODULE}.CreateExportRequest" in fields
    assert apicheck.proto_breakages(fields, fields) == []


def test_removed_and_renamed_fields_and_messages_are_reported() -> None:
    old = current()
    new = current()
    request = next(m for m in new.message_type if m.name == "CreateExportRequest")
    request.field[0].name = "renamed"
    removed = new.message_type[-1].name
    del new.message_type[-1]

    breakages = apicheck.proto_breakages(
        apicheck.message_fields({PB2: pb2_source(old)}, "src"),
        apicheck.message_fields({PB2: pb2_source(new)}, "src"),
    )

    old_request = next(m for m in old.message_type if m.name == "CreateExportRequest")
    field = f"{MODULE}.CreateExportRequest.{old_request.field[0].name}"
    assert (PB2, f"{field}: Proto field was removed") in breakages
    assert (PB2, f"{MODULE}.{removed}: Proto message was removed") in breakages
    assert len(breakages) == 2
