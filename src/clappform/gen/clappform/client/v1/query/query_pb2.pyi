from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from clappform.gen.clappform.client.v1.widget import widget_pb2 as _widget_pb2
from clappform.gen.clappform.client.v1.collection import collection_pb2 as _collection_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Query(_message.Message):
    __slots__ = ("id", "name", "pipeline", "source_query", "collection", "app", "created_at", "updated_at", "deleted_at", "versions", "exportable", "collection_data", "collection_rules")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_QUERY_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    EXPORTABLE_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_DATA_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_RULES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    pipeline: bytes
    source_query: Query
    collection: str
    app: str
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    exportable: bool
    collection_data: _collection_pb2.Collection
    collection_rules: _containers.RepeatedCompositeFieldContainer[_collection_pb2.CollectionRule]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., pipeline: _Optional[bytes] = ..., source_query: _Optional[_Union[Query, _Mapping]] = ..., collection: _Optional[str] = ..., app: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ..., exportable: bool = ..., collection_data: _Optional[_Union[_collection_pb2.Collection, _Mapping]] = ..., collection_rules: _Optional[_Iterable[_Union[_collection_pb2.CollectionRule, _Mapping]]] = ...) -> None: ...

class SourceQueryRequest(_message.Message):
    __slots__ = ("id", "page")
    ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    page: str
    def __init__(self, id: _Optional[str] = ..., page: _Optional[str] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("name", "pipeline", "source_query", "collection", "exportable")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_QUERY_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    EXPORTABLE_FIELD_NUMBER: _ClassVar[int]
    name: str
    pipeline: bytes
    source_query: str
    collection: str
    exportable: bool
    def __init__(self, name: _Optional[str] = ..., pipeline: _Optional[bytes] = ..., source_query: _Optional[str] = ..., collection: _Optional[str] = ..., exportable: bool = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "name", "pipeline", "source_query", "collection", "exportable")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_QUERY_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    EXPORTABLE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    pipeline: bytes
    source_query: str
    collection: str
    exportable: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., pipeline: _Optional[bytes] = ..., source_query: _Optional[str] = ..., collection: _Optional[str] = ..., exportable: bool = ...) -> None: ...

class Queries(_message.Message):
    __slots__ = ("queries", "pagination")
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    queries: _containers.RepeatedCompositeFieldContainer[Query]
    pagination: _commons_pb2.Pagination
    def __init__(self, queries: _Optional[_Iterable[_Union[Query, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
