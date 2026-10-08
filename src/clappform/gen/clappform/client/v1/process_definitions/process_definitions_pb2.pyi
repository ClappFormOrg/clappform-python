from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProcessDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TYPE_UNSPECIFIED: _ClassVar[ProcessDefinitionType]
    TYPE_QUESTIONNAIRE: _ClassVar[ProcessDefinitionType]
    TYPE_QUERY: _ClassVar[ProcessDefinitionType]
    TYPE_ACTIONFLOW: _ClassVar[ProcessDefinitionType]
TYPE_UNSPECIFIED: ProcessDefinitionType
TYPE_QUESTIONNAIRE: ProcessDefinitionType
TYPE_QUERY: ProcessDefinitionType
TYPE_ACTIONFLOW: ProcessDefinitionType

class ProcessDefinition(_message.Message):
    __slots__ = ("id", "name", "source_id", "type", "metadata", "created_at", "updated_at", "deleted_at", "versions")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    source_id: str
    type: ProcessDefinitionType
    metadata: _struct_pb2.Struct
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., source_id: _Optional[str] = ..., type: _Optional[_Union[ProcessDefinitionType, str]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("name", "source_id", "type", "metadata")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    source_id: str
    type: ProcessDefinitionType
    metadata: _struct_pb2.Struct
    def __init__(self, name: _Optional[str] = ..., source_id: _Optional[str] = ..., type: _Optional[_Union[ProcessDefinitionType, str]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "name", "source_id", "type", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    source_id: str
    type: ProcessDefinitionType
    metadata: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., source_id: _Optional[str] = ..., type: _Optional[_Union[ProcessDefinitionType, str]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ProcessDefinitions(_message.Message):
    __slots__ = ("process_definitions", "pagination")
    PROCESS_DEFINITIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    process_definitions: _containers.RepeatedCompositeFieldContainer[ProcessDefinition]
    pagination: _commons_pb2.Pagination
    def __init__(self, process_definitions: _Optional[_Iterable[_Union[ProcessDefinition, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
