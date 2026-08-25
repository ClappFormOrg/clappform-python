from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from clappform.gen.clappform.client.v1.actionflow_task import actionflow_task_pb2 as _actionflow_task_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Actionflow(_message.Message):
    __slots__ = ("id", "name", "settings", "start_keys", "fast", "multiple", "actionflow_tasks", "created_at", "updated_at", "deleted_at", "versions")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    START_KEYS_FIELD_NUMBER: _ClassVar[int]
    FAST_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_FIELD_NUMBER: _ClassVar[int]
    ACTIONFLOW_TASKS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    settings: bytes
    start_keys: bytes
    fast: bool
    multiple: bool
    actionflow_tasks: _containers.RepeatedScalarFieldContainer[str]
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ..., start_keys: _Optional[bytes] = ..., fast: bool = ..., multiple: bool = ..., actionflow_tasks: _Optional[_Iterable[str]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("name", "settings", "start_keys", "fast", "multiple", "actionflow_tasks")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    START_KEYS_FIELD_NUMBER: _ClassVar[int]
    FAST_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_FIELD_NUMBER: _ClassVar[int]
    ACTIONFLOW_TASKS_FIELD_NUMBER: _ClassVar[int]
    name: str
    settings: bytes
    start_keys: bytes
    fast: bool
    multiple: bool
    actionflow_tasks: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., settings: _Optional[bytes] = ..., start_keys: _Optional[bytes] = ..., fast: bool = ..., multiple: bool = ..., actionflow_tasks: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "name", "settings", "start_keys", "fast", "multiple", "actionflow_tasks")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    START_KEYS_FIELD_NUMBER: _ClassVar[int]
    FAST_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_FIELD_NUMBER: _ClassVar[int]
    ACTIONFLOW_TASKS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    settings: bytes
    start_keys: bytes
    fast: bool
    multiple: bool
    actionflow_tasks: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ..., start_keys: _Optional[bytes] = ..., fast: bool = ..., multiple: bool = ..., actionflow_tasks: _Optional[_Iterable[str]] = ...) -> None: ...

class Actionflows(_message.Message):
    __slots__ = ("actionflows", "actionflow_tasks", "pagination")
    ACTIONFLOWS_FIELD_NUMBER: _ClassVar[int]
    ACTIONFLOW_TASKS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    actionflows: _containers.RepeatedCompositeFieldContainer[Actionflow]
    actionflow_tasks: _containers.RepeatedCompositeFieldContainer[_actionflow_task_pb2.ActionflowTask]
    pagination: _commons_pb2.Pagination
    def __init__(self, actionflows: _Optional[_Iterable[_Union[Actionflow, _Mapping]]] = ..., actionflow_tasks: _Optional[_Iterable[_Union[_actionflow_task_pb2.ActionflowTask, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...

class StartActionflow(_message.Message):
    __slots__ = ("id", "user_id", "custom_keys")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_KEYS_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    custom_keys: bytes
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., custom_keys: _Optional[bytes] = ...) -> None: ...

class StartActionflowResponse(_message.Message):
    __slots__ = ("message", "uuid")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    message: str
    uuid: str
    def __init__(self, message: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...
