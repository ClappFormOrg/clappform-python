from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class taskType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[taskType]
    TEMPLATE: _ClassVar[taskType]
    MODULE: _ClassVar[taskType]
UNSPECIFIED: taskType
TEMPLATE: taskType
MODULE: taskType

class ActionflowTask(_message.Message):
    __slots__ = ("id", "name", "settings", "input", "output", "type", "script", "timeout", "actionflows", "created_at", "updated_at", "deleted_at", "versions")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    ACTIONFLOWS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    settings: bytes
    input: bytes
    output: bytes
    type: str
    script: bytes
    timeout: int
    actionflows: _containers.RepeatedScalarFieldContainer[str]
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ..., input: _Optional[bytes] = ..., output: _Optional[bytes] = ..., type: _Optional[str] = ..., script: _Optional[bytes] = ..., timeout: _Optional[int] = ..., actionflows: _Optional[_Iterable[str]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("name", "settings", "input", "output", "type", "script", "timeout")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    name: str
    settings: bytes
    input: bytes
    output: bytes
    type: taskType
    script: bytes
    timeout: int
    def __init__(self, name: _Optional[str] = ..., settings: _Optional[bytes] = ..., input: _Optional[bytes] = ..., output: _Optional[bytes] = ..., type: _Optional[_Union[taskType, str]] = ..., script: _Optional[bytes] = ..., timeout: _Optional[int] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "name", "settings", "input", "output", "type", "script", "timeout")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    settings: bytes
    input: bytes
    output: bytes
    type: taskType
    script: bytes
    timeout: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ..., input: _Optional[bytes] = ..., output: _Optional[bytes] = ..., type: _Optional[_Union[taskType, str]] = ..., script: _Optional[bytes] = ..., timeout: _Optional[int] = ...) -> None: ...

class ActionflowTasks(_message.Message):
    __slots__ = ("actionflow_tasks", "pagination")
    ACTIONFLOW_TASKS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    actionflow_tasks: _containers.RepeatedCompositeFieldContainer[ActionflowTask]
    pagination: _commons_pb2.Pagination
    def __init__(self, actionflow_tasks: _Optional[_Iterable[_Union[ActionflowTask, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
