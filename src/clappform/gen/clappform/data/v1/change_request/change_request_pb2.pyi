from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChangeRequest(_message.Message):
    __slots__ = ("data", "collection")
    DATA_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    collection: str
    def __init__(self, data: _Optional[bytes] = ..., collection: _Optional[str] = ...) -> None: ...

class RequestChangeResponse(_message.Message):
    __slots__ = ("request_id",)
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    def __init__(self, request_id: _Optional[str] = ...) -> None: ...

class UpdateStatusRequest(_message.Message):
    __slots__ = ("request_id", "collection", "note")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    collection: str
    note: str
    def __init__(self, request_id: _Optional[str] = ..., collection: _Optional[str] = ..., note: _Optional[str] = ...) -> None: ...

class ModifyChangeRequest(_message.Message):
    __slots__ = ("request_id", "collection", "note", "data")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    collection: str
    note: str
    data: bytes
    def __init__(self, request_id: _Optional[str] = ..., collection: _Optional[str] = ..., note: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class ModifyApproverRequest(_message.Message):
    __slots__ = ("request_id", "collection", "note", "approver_id")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    APPROVER_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    collection: str
    note: str
    approver_id: str
    def __init__(self, request_id: _Optional[str] = ..., collection: _Optional[str] = ..., note: _Optional[str] = ..., approver_id: _Optional[str] = ...) -> None: ...
