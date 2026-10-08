from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileWatcher(_message.Message):
    __slots__ = ("id", "name", "patterns", "directory", "commands", "environment", "ignore_directories", "ignore_patterns", "timeout", "recursive", "events", "created_at", "updated_at", "deleted_at", "versions")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATTERNS_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    IGNORE_DIRECTORIES_FIELD_NUMBER: _ClassVar[int]
    IGNORE_PATTERNS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    RECURSIVE_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    patterns: _containers.RepeatedScalarFieldContainer[str]
    directory: str
    commands: _containers.RepeatedScalarFieldContainer[str]
    environment: bytes
    ignore_directories: bool
    ignore_patterns: _containers.RepeatedScalarFieldContainer[str]
    timeout: int
    recursive: bool
    events: _containers.RepeatedScalarFieldContainer[str]
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., patterns: _Optional[_Iterable[str]] = ..., directory: _Optional[str] = ..., commands: _Optional[_Iterable[str]] = ..., environment: _Optional[bytes] = ..., ignore_directories: bool = ..., ignore_patterns: _Optional[_Iterable[str]] = ..., timeout: _Optional[int] = ..., recursive: bool = ..., events: _Optional[_Iterable[str]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("name", "patterns", "directory", "commands", "environment", "ignore_directories", "ignore_patterns", "timeout", "recursive", "events")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATTERNS_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    IGNORE_DIRECTORIES_FIELD_NUMBER: _ClassVar[int]
    IGNORE_PATTERNS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    RECURSIVE_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    patterns: _containers.RepeatedScalarFieldContainer[str]
    directory: str
    commands: _containers.RepeatedScalarFieldContainer[str]
    environment: bytes
    ignore_directories: bool
    ignore_patterns: _containers.RepeatedScalarFieldContainer[str]
    timeout: int
    recursive: bool
    events: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., patterns: _Optional[_Iterable[str]] = ..., directory: _Optional[str] = ..., commands: _Optional[_Iterable[str]] = ..., environment: _Optional[bytes] = ..., ignore_directories: bool = ..., ignore_patterns: _Optional[_Iterable[str]] = ..., timeout: _Optional[int] = ..., recursive: bool = ..., events: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "name", "patterns", "directory", "commands", "environment", "ignore_directories", "ignore_patterns", "timeout", "recursive", "events")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATTERNS_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    IGNORE_DIRECTORIES_FIELD_NUMBER: _ClassVar[int]
    IGNORE_PATTERNS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    RECURSIVE_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    patterns: _containers.RepeatedScalarFieldContainer[str]
    directory: str
    commands: _containers.RepeatedScalarFieldContainer[str]
    environment: bytes
    ignore_directories: bool
    ignore_patterns: _containers.RepeatedScalarFieldContainer[str]
    timeout: int
    recursive: bool
    events: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., patterns: _Optional[_Iterable[str]] = ..., directory: _Optional[str] = ..., commands: _Optional[_Iterable[str]] = ..., environment: _Optional[bytes] = ..., ignore_directories: bool = ..., ignore_patterns: _Optional[_Iterable[str]] = ..., timeout: _Optional[int] = ..., recursive: bool = ..., events: _Optional[_Iterable[str]] = ...) -> None: ...

class FileWatchers(_message.Message):
    __slots__ = ("file_watchers", "pagination")
    FILE_WATCHERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    file_watchers: _containers.RepeatedCompositeFieldContainer[FileWatcher]
    pagination: _commons_pb2.Pagination
    def __init__(self, file_watchers: _Optional[_Iterable[_Union[FileWatcher, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
