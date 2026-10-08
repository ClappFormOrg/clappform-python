from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PatchResponse(_message.Message):
    __slots__ = ("oid",)
    OID_FIELD_NUMBER: _ClassVar[int]
    oid: str
    def __init__(self, oid: _Optional[str] = ...) -> None: ...

class InsertRequest(_message.Message):
    __slots__ = ("data", "collection")
    DATA_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    collection: str
    def __init__(self, data: _Optional[bytes] = ..., collection: _Optional[str] = ...) -> None: ...

class InsertResponse(_message.Message):
    __slots__ = ("processed_count", "oids", "data")
    PROCESSED_COUNT_FIELD_NUMBER: _ClassVar[int]
    OIDS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    processed_count: int
    oids: _containers.RepeatedScalarFieldContainer[str]
    data: bytes
    def __init__(self, processed_count: _Optional[int] = ..., oids: _Optional[_Iterable[str]] = ..., data: _Optional[bytes] = ...) -> None: ...
