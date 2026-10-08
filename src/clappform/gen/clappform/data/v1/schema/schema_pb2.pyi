from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CollectionSchemaRequest(_message.Message):
    __slots__ = ("collection_id", "sample_size", "include_distribution", "include_sample_values")
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_SIZE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SAMPLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    collection_id: str
    sample_size: int
    include_distribution: bool
    include_sample_values: bool
    def __init__(self, collection_id: _Optional[str] = ..., sample_size: _Optional[int] = ..., include_distribution: bool = ..., include_sample_values: bool = ...) -> None: ...

class CollectionSchemaResponse(_message.Message):
    __slots__ = ("collection_id", "collection_slug", "sampled_documents", "fields")
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_SLUG_FIELD_NUMBER: _ClassVar[int]
    SAMPLED_DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    collection_id: str
    collection_slug: str
    sampled_documents: int
    fields: _containers.RepeatedCompositeFieldContainer[SchemaField]
    def __init__(self, collection_id: _Optional[str] = ..., collection_slug: _Optional[str] = ..., sampled_documents: _Optional[int] = ..., fields: _Optional[_Iterable[_Union[SchemaField, _Mapping]]] = ...) -> None: ...

class QuerySchemaRequest(_message.Message):
    __slots__ = ("query_id", "collection_id", "inline_pipeline", "sample_size", "include_distribution", "include_sample_values")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    INLINE_PIPELINE_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_SIZE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SAMPLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    collection_id: str
    inline_pipeline: bytes
    sample_size: int
    include_distribution: bool
    include_sample_values: bool
    def __init__(self, query_id: _Optional[str] = ..., collection_id: _Optional[str] = ..., inline_pipeline: _Optional[bytes] = ..., sample_size: _Optional[int] = ..., include_distribution: bool = ..., include_sample_values: bool = ...) -> None: ...

class QuerySchemaResponse(_message.Message):
    __slots__ = ("query_id", "collection_id", "collection_slug", "sampled_documents", "fields")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_SLUG_FIELD_NUMBER: _ClassVar[int]
    SAMPLED_DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    collection_id: str
    collection_slug: str
    sampled_documents: int
    fields: _containers.RepeatedCompositeFieldContainer[SchemaField]
    def __init__(self, query_id: _Optional[str] = ..., collection_id: _Optional[str] = ..., collection_slug: _Optional[str] = ..., sampled_documents: _Optional[int] = ..., fields: _Optional[_Iterable[_Union[SchemaField, _Mapping]]] = ...) -> None: ...

class CollectionInfoRequest(_message.Message):
    __slots__ = ("collection_id",)
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    collection_id: str
    def __init__(self, collection_id: _Optional[str] = ...) -> None: ...

class CollectionInfoResponse(_message.Message):
    __slots__ = ("collection_id", "collection_slug", "database_type", "document_count", "storage_size_bytes", "last_write_at", "schema_sampled_at", "collection_rules_count", "index_count", "read_count_30d", "unique_readers_30d", "last_read_at")
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_SLUG_FIELD_NUMBER: _ClassVar[int]
    DATABASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    STORAGE_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    LAST_WRITE_AT_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_SAMPLED_AT_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_RULES_COUNT_FIELD_NUMBER: _ClassVar[int]
    INDEX_COUNT_FIELD_NUMBER: _ClassVar[int]
    READ_COUNT_30D_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_READERS_30D_FIELD_NUMBER: _ClassVar[int]
    LAST_READ_AT_FIELD_NUMBER: _ClassVar[int]
    collection_id: str
    collection_slug: str
    database_type: str
    document_count: int
    storage_size_bytes: int
    last_write_at: _timestamp_pb2.Timestamp
    schema_sampled_at: _timestamp_pb2.Timestamp
    collection_rules_count: int
    index_count: int
    read_count_30d: int
    unique_readers_30d: int
    last_read_at: _timestamp_pb2.Timestamp
    def __init__(self, collection_id: _Optional[str] = ..., collection_slug: _Optional[str] = ..., database_type: _Optional[str] = ..., document_count: _Optional[int] = ..., storage_size_bytes: _Optional[int] = ..., last_write_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., schema_sampled_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., collection_rules_count: _Optional[int] = ..., index_count: _Optional[int] = ..., read_count_30d: _Optional[int] = ..., unique_readers_30d: _Optional[int] = ..., last_read_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class BuildFKGraphRequest(_message.Message):
    __slots__ = ("app_id", "sample_size")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_SIZE_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    sample_size: int
    def __init__(self, app_id: _Optional[str] = ..., sample_size: _Optional[int] = ...) -> None: ...

class FKLink(_message.Message):
    __slots__ = ("from_collection", "from_field", "to_collection", "value_field", "label_field")
    FROM_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_FIELD_NUMBER: _ClassVar[int]
    TO_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_FIELD_NUMBER: _ClassVar[int]
    from_collection: str
    from_field: str
    to_collection: str
    value_field: str
    label_field: str
    def __init__(self, from_collection: _Optional[str] = ..., from_field: _Optional[str] = ..., to_collection: _Optional[str] = ..., value_field: _Optional[str] = ..., label_field: _Optional[str] = ...) -> None: ...

class BuildFKGraphResponse(_message.Message):
    __slots__ = ("generated_at", "collections_scanned", "links")
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    COLLECTIONS_SCANNED_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    generated_at: _timestamp_pb2.Timestamp
    collections_scanned: int
    links: _containers.RepeatedCompositeFieldContainer[FKLink]
    def __init__(self, generated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., collections_scanned: _Optional[int] = ..., links: _Optional[_Iterable[_Union[FKLink, _Mapping]]] = ...) -> None: ...

class GetFKGraphRequest(_message.Message):
    __slots__ = ("app_id",)
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    def __init__(self, app_id: _Optional[str] = ...) -> None: ...

class GetFKGraphResponse(_message.Message):
    __slots__ = ("generated_at", "links")
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    generated_at: _timestamp_pb2.Timestamp
    links: _containers.RepeatedCompositeFieldContainer[FKLink]
    def __init__(self, generated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., links: _Optional[_Iterable[_Union[FKLink, _Mapping]]] = ...) -> None: ...

class SchemaField(_message.Message):
    __slots__ = ("key", "types_found", "cardinality", "null_percentage", "appears_in_percentage", "distribution", "sample_values")
    KEY_FIELD_NUMBER: _ClassVar[int]
    TYPES_FOUND_FIELD_NUMBER: _ClassVar[int]
    CARDINALITY_FIELD_NUMBER: _ClassVar[int]
    NULL_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    APPEARS_IN_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    key: str
    types_found: _containers.RepeatedScalarFieldContainer[str]
    cardinality: int
    null_percentage: float
    appears_in_percentage: float
    distribution: Distribution
    sample_values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, key: _Optional[str] = ..., types_found: _Optional[_Iterable[str]] = ..., cardinality: _Optional[int] = ..., null_percentage: _Optional[float] = ..., appears_in_percentage: _Optional[float] = ..., distribution: _Optional[_Union[Distribution, _Mapping]] = ..., sample_values: _Optional[_Iterable[str]] = ...) -> None: ...

class Distribution(_message.Message):
    __slots__ = ("categorical", "numeric", "bool", "date")
    CATEGORICAL_FIELD_NUMBER: _ClassVar[int]
    NUMERIC_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    categorical: CategoricalDistribution
    numeric: NumericDistribution
    bool: BoolDistribution
    date: DateDistribution
    def __init__(self, categorical: _Optional[_Union[CategoricalDistribution, _Mapping]] = ..., numeric: _Optional[_Union[NumericDistribution, _Mapping]] = ..., bool: _Optional[_Union[BoolDistribution, _Mapping]] = ..., date: _Optional[_Union[DateDistribution, _Mapping]] = ...) -> None: ...

class CategoricalDistribution(_message.Message):
    __slots__ = ("top", "other_count")
    TOP_FIELD_NUMBER: _ClassVar[int]
    OTHER_COUNT_FIELD_NUMBER: _ClassVar[int]
    top: _containers.RepeatedCompositeFieldContainer[CategoricalBucket]
    other_count: int
    def __init__(self, top: _Optional[_Iterable[_Union[CategoricalBucket, _Mapping]]] = ..., other_count: _Optional[int] = ...) -> None: ...

class CategoricalBucket(_message.Message):
    __slots__ = ("value", "count")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    value: str
    count: int
    def __init__(self, value: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class NumericDistribution(_message.Message):
    __slots__ = ("min", "max", "mean", "buckets")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    min: float
    max: float
    mean: float
    buckets: _containers.RepeatedCompositeFieldContainer[NumericBucket]
    def __init__(self, min: _Optional[float] = ..., max: _Optional[float] = ..., mean: _Optional[float] = ..., buckets: _Optional[_Iterable[_Union[NumericBucket, _Mapping]]] = ...) -> None: ...

class NumericBucket(_message.Message):
    __slots__ = ("lower", "upper", "count")
    LOWER_FIELD_NUMBER: _ClassVar[int]
    UPPER_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    lower: float
    upper: float
    count: int
    def __init__(self, lower: _Optional[float] = ..., upper: _Optional[float] = ..., count: _Optional[int] = ...) -> None: ...

class BoolDistribution(_message.Message):
    __slots__ = ("true_count", "false_count")
    TRUE_COUNT_FIELD_NUMBER: _ClassVar[int]
    FALSE_COUNT_FIELD_NUMBER: _ClassVar[int]
    true_count: int
    false_count: int
    def __init__(self, true_count: _Optional[int] = ..., false_count: _Optional[int] = ...) -> None: ...

class DateDistribution(_message.Message):
    __slots__ = ("min_unix_nano", "max_unix_nano", "buckets")
    MIN_UNIX_NANO_FIELD_NUMBER: _ClassVar[int]
    MAX_UNIX_NANO_FIELD_NUMBER: _ClassVar[int]
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    min_unix_nano: int
    max_unix_nano: int
    buckets: _containers.RepeatedCompositeFieldContainer[DateBucket]
    def __init__(self, min_unix_nano: _Optional[int] = ..., max_unix_nano: _Optional[int] = ..., buckets: _Optional[_Iterable[_Union[DateBucket, _Mapping]]] = ...) -> None: ...

class DateBucket(_message.Message):
    __slots__ = ("lower_unix_nano", "upper_unix_nano", "count")
    LOWER_UNIX_NANO_FIELD_NUMBER: _ClassVar[int]
    UPPER_UNIX_NANO_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    lower_unix_nano: int
    upper_unix_nano: int
    count: int
    def __init__(self, lower_unix_nano: _Optional[int] = ..., upper_unix_nano: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
