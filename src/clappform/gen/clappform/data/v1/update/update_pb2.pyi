from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateRequestByOid(_message.Message):
    __slots__ = ("data", "collection")
    DATA_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    collection: str
    def __init__(self, data: _Optional[bytes] = ..., collection: _Optional[str] = ...) -> None: ...

class UpdateRequestByField(_message.Message):
    __slots__ = ("data", "collection", "field_name")
    DATA_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    collection: str
    field_name: str
    def __init__(self, data: _Optional[bytes] = ..., collection: _Optional[str] = ..., field_name: _Optional[str] = ...) -> None: ...

class UpdateRequestByQuery(_message.Message):
    __slots__ = ("set_values", "collection", "query")
    SET_VALUES_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    set_values: bytes
    collection: str
    query: bytes
    def __init__(self, set_values: _Optional[bytes] = ..., collection: _Optional[str] = ..., query: _Optional[bytes] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("data", "collection")
    DATA_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    collection: str
    def __init__(self, data: _Optional[bytes] = ..., collection: _Optional[str] = ...) -> None: ...

class UpdateRequestResponse(_message.Message):
    __slots__ = ("data", "collection")
    DATA_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    collection: str
    def __init__(self, data: _Optional[bytes] = ..., collection: _Optional[str] = ...) -> None: ...
