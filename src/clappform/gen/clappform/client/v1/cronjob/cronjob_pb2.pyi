from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Cronjob(_message.Message):
    __slots__ = ("id", "name", "pattern", "settings", "actionflows", "status", "created_at", "updated_at", "deleted_at", "versions")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ACTIONFLOWS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    pattern: str
    settings: bytes
    actionflows: _containers.RepeatedScalarFieldContainer[str]
    status: Status
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., pattern: _Optional[str] = ..., settings: _Optional[bytes] = ..., actionflows: _Optional[_Iterable[str]] = ..., status: _Optional[_Union[Status, _Mapping]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ("prev_run", "next_run", "is_running", "run_id")
    PREV_RUN_FIELD_NUMBER: _ClassVar[int]
    NEXT_RUN_FIELD_NUMBER: _ClassVar[int]
    IS_RUNNING_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    prev_run: str
    next_run: str
    is_running: bool
    run_id: int
    def __init__(self, prev_run: _Optional[str] = ..., next_run: _Optional[str] = ..., is_running: bool = ..., run_id: _Optional[int] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("name", "pattern", "settings", "actionflows")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ACTIONFLOWS_FIELD_NUMBER: _ClassVar[int]
    name: str
    pattern: str
    settings: bytes
    actionflows: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., pattern: _Optional[str] = ..., settings: _Optional[bytes] = ..., actionflows: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "name", "pattern", "settings", "actionflows")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ACTIONFLOWS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    pattern: str
    settings: bytes
    actionflows: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., pattern: _Optional[str] = ..., settings: _Optional[bytes] = ..., actionflows: _Optional[_Iterable[str]] = ...) -> None: ...

class Cronjobs(_message.Message):
    __slots__ = ("cronjobs", "pagination")
    CRONJOBS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    cronjobs: _containers.RepeatedCompositeFieldContainer[Cronjob]
    pagination: _commons_pb2.Pagination
    def __init__(self, cronjobs: _Optional[_Iterable[_Union[Cronjob, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
