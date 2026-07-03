from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteRequestOids(_message.Message):
    __slots__ = ("oids", "collection")
    OIDS_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    oids: _containers.RepeatedScalarFieldContainer[str]
    collection: str
    def __init__(self, oids: _Optional[_Iterable[str]] = ..., collection: _Optional[str] = ...) -> None: ...

class DeleteRequestByField(_message.Message):
    __slots__ = ("ids", "collection", "field_name")
    IDS_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    ids: bytes
    collection: str
    field_name: str
    def __init__(self, ids: _Optional[bytes] = ..., collection: _Optional[str] = ..., field_name: _Optional[str] = ...) -> None: ...

class DeleteRequestQuery(_message.Message):
    __slots__ = ("query", "collection", "dry_run")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    query: bytes
    collection: str
    dry_run: bool
    def __init__(self, query: _Optional[bytes] = ..., collection: _Optional[str] = ..., dry_run: bool = ...) -> None: ...

class ClearRequest(_message.Message):
    __slots__ = ("collection",)
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    collection: str
    def __init__(self, collection: _Optional[str] = ...) -> None: ...

class DataResponse(_message.Message):
    __slots__ = ("data", "total", "total_sent")
    DATA_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SENT_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    total: int
    total_sent: int
    def __init__(self, data: _Optional[bytes] = ..., total: _Optional[int] = ..., total_sent: _Optional[int] = ...) -> None: ...
