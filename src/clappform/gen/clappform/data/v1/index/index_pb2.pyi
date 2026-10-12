from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListIndexesRequest(_message.Message):
    __slots__ = ("collection",)
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    collection: str
    def __init__(self, collection: _Optional[str] = ...) -> None: ...

class IndexStats(_message.Message):
    __slots__ = ("entries", "size_bytes", "type", "accesses_ops", "builds", "usage_since", "docs_count", "deleted_docs", "segments_count", "search_query_total", "indexing_total")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCESSES_OPS_FIELD_NUMBER: _ClassVar[int]
    BUILDS_FIELD_NUMBER: _ClassVar[int]
    USAGE_SINCE_FIELD_NUMBER: _ClassVar[int]
    DOCS_COUNT_FIELD_NUMBER: _ClassVar[int]
    DELETED_DOCS_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_COUNT_FIELD_NUMBER: _ClassVar[int]
    SEARCH_QUERY_TOTAL_FIELD_NUMBER: _ClassVar[int]
    INDEXING_TOTAL_FIELD_NUMBER: _ClassVar[int]
    entries: int
    size_bytes: int
    type: str
    accesses_ops: int
    builds: int
    usage_since: int
    docs_count: int
    deleted_docs: int
    segments_count: int
    search_query_total: int
    indexing_total: int
    def __init__(self, entries: _Optional[int] = ..., size_bytes: _Optional[int] = ..., type: _Optional[str] = ..., accesses_ops: _Optional[int] = ..., builds: _Optional[int] = ..., usage_since: _Optional[int] = ..., docs_count: _Optional[int] = ..., deleted_docs: _Optional[int] = ..., segments_count: _Optional[int] = ..., search_query_total: _Optional[int] = ..., indexing_total: _Optional[int] = ...) -> None: ...

class IndexInfo(_message.Message):
    __slots__ = ("name", "keys", "stats")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    name: str
    keys: _containers.RepeatedCompositeFieldContainer[IndexKey]
    stats: IndexStats
    def __init__(self, name: _Optional[str] = ..., keys: _Optional[_Iterable[_Union[IndexKey, _Mapping]]] = ..., stats: _Optional[_Union[IndexStats, _Mapping]] = ...) -> None: ...

class ListIndexesResponse(_message.Message):
    __slots__ = ("indexes",)
    INDEXES_FIELD_NUMBER: _ClassVar[int]
    indexes: _containers.RepeatedCompositeFieldContainer[IndexInfo]
    def __init__(self, indexes: _Optional[_Iterable[_Union[IndexInfo, _Mapping]]] = ...) -> None: ...

class CreateIndexRequest(_message.Message):
    __slots__ = ("collection", "index_name", "mongo_index_model", "elastic_settings")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    MONGO_INDEX_MODEL_FIELD_NUMBER: _ClassVar[int]
    ELASTIC_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    collection: str
    index_name: str
    mongo_index_model: MongoIndexModel
    elastic_settings: bytes
    def __init__(self, collection: _Optional[str] = ..., index_name: _Optional[str] = ..., mongo_index_model: _Optional[_Union[MongoIndexModel, _Mapping]] = ..., elastic_settings: _Optional[bytes] = ...) -> None: ...

class CreateIndexResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class DeleteIndexRequest(_message.Message):
    __slots__ = ("collection", "index_name")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    collection: str
    index_name: str
    def __init__(self, collection: _Optional[str] = ..., index_name: _Optional[str] = ...) -> None: ...

class DeleteIndexResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class GetIndexDetailsRequest(_message.Message):
    __slots__ = ("collection", "index_name")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    collection: str
    index_name: str
    def __init__(self, collection: _Optional[str] = ..., index_name: _Optional[str] = ...) -> None: ...

class GetIndexDetailsResponse(_message.Message):
    __slots__ = ("details", "stats")
    class IndexStats(_message.Message):
        __slots__ = ("entries", "size_bytes", "type", "accesses_ops", "builds", "usage_since", "docs_count", "deleted_docs", "segments_count", "search_query_total", "indexing_total")
        ENTRIES_FIELD_NUMBER: _ClassVar[int]
        SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        ACCESSES_OPS_FIELD_NUMBER: _ClassVar[int]
        BUILDS_FIELD_NUMBER: _ClassVar[int]
        USAGE_SINCE_FIELD_NUMBER: _ClassVar[int]
        DOCS_COUNT_FIELD_NUMBER: _ClassVar[int]
        DELETED_DOCS_FIELD_NUMBER: _ClassVar[int]
        SEGMENTS_COUNT_FIELD_NUMBER: _ClassVar[int]
        SEARCH_QUERY_TOTAL_FIELD_NUMBER: _ClassVar[int]
        INDEXING_TOTAL_FIELD_NUMBER: _ClassVar[int]
        entries: int
        size_bytes: int
        type: str
        accesses_ops: int
        builds: int
        usage_since: int
        docs_count: int
        deleted_docs: int
        segments_count: int
        search_query_total: int
        indexing_total: int
        def __init__(self, entries: _Optional[int] = ..., size_bytes: _Optional[int] = ..., type: _Optional[str] = ..., accesses_ops: _Optional[int] = ..., builds: _Optional[int] = ..., usage_since: _Optional[int] = ..., docs_count: _Optional[int] = ..., deleted_docs: _Optional[int] = ..., segments_count: _Optional[int] = ..., search_query_total: _Optional[int] = ..., indexing_total: _Optional[int] = ...) -> None: ...
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    details: bytes
    stats: GetIndexDetailsResponse.IndexStats
    def __init__(self, details: _Optional[bytes] = ..., stats: _Optional[_Union[GetIndexDetailsResponse.IndexStats, _Mapping]] = ...) -> None: ...

class UpdateIndexRequest(_message.Message):
    __slots__ = ("collection", "index_name", "mongo_index_model", "elastic_settings")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    MONGO_INDEX_MODEL_FIELD_NUMBER: _ClassVar[int]
    ELASTIC_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    collection: str
    index_name: str
    mongo_index_model: MongoIndexModel
    elastic_settings: bytes
    def __init__(self, collection: _Optional[str] = ..., index_name: _Optional[str] = ..., mongo_index_model: _Optional[_Union[MongoIndexModel, _Mapping]] = ..., elastic_settings: _Optional[bytes] = ...) -> None: ...

class UpdateIndexResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class IndexKey(_message.Message):
    __slots__ = ("field", "order", "type")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    field: str
    order: int
    type: str
    def __init__(self, field: _Optional[str] = ..., order: _Optional[int] = ..., type: _Optional[str] = ...) -> None: ...

class PartialFilterExpression(_message.Message):
    __slots__ = ("filters",)
    class FiltersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: _containers.ScalarMap[str, str]
    def __init__(self, filters: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Collation(_message.Message):
    __slots__ = ("locale", "case_level", "case_first", "strength", "numeric_ordering", "alternate", "max_variable", "backwards")
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    CASE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CASE_FIRST_FIELD_NUMBER: _ClassVar[int]
    STRENGTH_FIELD_NUMBER: _ClassVar[int]
    NUMERIC_ORDERING_FIELD_NUMBER: _ClassVar[int]
    ALTERNATE_FIELD_NUMBER: _ClassVar[int]
    MAX_VARIABLE_FIELD_NUMBER: _ClassVar[int]
    BACKWARDS_FIELD_NUMBER: _ClassVar[int]
    locale: str
    case_level: bool
    case_first: str
    strength: int
    numeric_ordering: bool
    alternate: str
    max_variable: str
    backwards: bool
    def __init__(self, locale: _Optional[str] = ..., case_level: bool = ..., case_first: _Optional[str] = ..., strength: _Optional[int] = ..., numeric_ordering: bool = ..., alternate: _Optional[str] = ..., max_variable: _Optional[str] = ..., backwards: bool = ...) -> None: ...

class MongoIndexModel(_message.Message):
    __slots__ = ("name", "keys", "unique", "sparse", "expire_after_seconds", "partial_filter_expression", "collation")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_FIELD_NUMBER: _ClassVar[int]
    SPARSE_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AFTER_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_FILTER_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    COLLATION_FIELD_NUMBER: _ClassVar[int]
    name: str
    keys: _containers.RepeatedCompositeFieldContainer[IndexKey]
    unique: bool
    sparse: bool
    expire_after_seconds: int
    partial_filter_expression: PartialFilterExpression
    collation: Collation
    def __init__(self, name: _Optional[str] = ..., keys: _Optional[_Iterable[_Union[IndexKey, _Mapping]]] = ..., unique: bool = ..., sparse: bool = ..., expire_after_seconds: _Optional[int] = ..., partial_filter_expression: _Optional[_Union[PartialFilterExpression, _Mapping]] = ..., collation: _Optional[_Union[Collation, _Mapping]] = ...) -> None: ...
