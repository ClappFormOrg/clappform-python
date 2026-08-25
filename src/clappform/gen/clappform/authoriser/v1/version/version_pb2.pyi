from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Version(_message.Message):
    __slots__ = ("id", "settings", "locked", "owner_id", "owner_type", "created_at", "updated_at", "deleted_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    settings: bytes
    locked: bool
    owner_id: str
    owner_type: str
    created_at: str
    updated_at: str
    deleted_at: str
    def __init__(self, id: _Optional[str] = ..., settings: _Optional[bytes] = ..., locked: bool = ..., owner_id: _Optional[str] = ..., owner_type: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ...) -> None: ...

class Versions(_message.Message):
    __slots__ = ("versions", "pagination")
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    versions: _containers.RepeatedCompositeFieldContainer[Version]
    pagination: _commons_pb2.Pagination
    def __init__(self, versions: _Optional[_Iterable[_Union[Version, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
