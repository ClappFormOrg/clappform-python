from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class granularityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[granularityType]
    NONE: _ClassVar[granularityType]
    R5: _ClassVar[granularityType]
    R10: _ClassVar[granularityType]
    R20: _ClassVar[granularityType]
    R40: _ClassVar[granularityType]
    R80: _ClassVar[granularityType]
    ONETWOFIVE: _ClassVar[granularityType]
    E6: _ClassVar[granularityType]
    E12: _ClassVar[granularityType]
    E24: _ClassVar[granularityType]
    E48: _ClassVar[granularityType]
    E96: _ClassVar[granularityType]
    E192: _ClassVar[granularityType]
    POWERSOF2: _ClassVar[granularityType]
UNSPECIFIED: granularityType
NONE: granularityType
R5: granularityType
R10: granularityType
R20: granularityType
R40: granularityType
R80: granularityType
ONETWOFIVE: granularityType
E6: granularityType
E12: granularityType
E24: granularityType
E48: granularityType
E96: granularityType
E192: granularityType
POWERSOF2: granularityType

class AggregateFilterOptions(_message.Message):
    __slots__ = ("keys", "name", "main_key", "selected_options", "type", "bucket_amount", "label_key", "granularity")
    KEYS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MAIN_KEY_FIELD_NUMBER: _ClassVar[int]
    SELECTED_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    LABEL_KEY_FIELD_NUMBER: _ClassVar[int]
    GRANULARITY_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    name: str
    main_key: str
    selected_options: bytes
    type: str
    bucket_amount: int
    label_key: str
    granularity: granularityType
    def __init__(self, keys: _Optional[_Iterable[str]] = ..., name: _Optional[str] = ..., main_key: _Optional[str] = ..., selected_options: _Optional[bytes] = ..., type: _Optional[str] = ..., bucket_amount: _Optional[int] = ..., label_key: _Optional[str] = ..., granularity: _Optional[_Union[granularityType, str]] = ...) -> None: ...

class AggregateStreamRequest(_message.Message):
    __slots__ = ("pipeline", "batch_size", "collection", "query")
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    pipeline: bytes
    batch_size: int
    collection: str
    query: str
    def __init__(self, pipeline: _Optional[bytes] = ..., batch_size: _Optional[int] = ..., collection: _Optional[str] = ..., query: _Optional[str] = ...) -> None: ...

class AggregateUnaryRequest(_message.Message):
    __slots__ = ("pipeline", "batch_size", "collection", "query", "filter_options", "deep_dive", "options", "inner_options", "next_page", "search", "bounds", "sorting", "explain", "custom_match")
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    FILTER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    DEEP_DIVE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    INNER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    SORTING_FIELD_NUMBER: _ClassVar[int]
    EXPLAIN_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MATCH_FIELD_NUMBER: _ClassVar[int]
    pipeline: bytes
    batch_size: int
    collection: str
    query: str
    filter_options: AggregateFilterOptions
    deep_dive: bytes
    options: bytes
    inner_options: bytes
    next_page: int
    search: bytes
    bounds: BoundsRequest
    sorting: bytes
    explain: bool
    custom_match: bytes
    def __init__(self, pipeline: _Optional[bytes] = ..., batch_size: _Optional[int] = ..., collection: _Optional[str] = ..., query: _Optional[str] = ..., filter_options: _Optional[_Union[AggregateFilterOptions, _Mapping]] = ..., deep_dive: _Optional[bytes] = ..., options: _Optional[bytes] = ..., inner_options: _Optional[bytes] = ..., next_page: _Optional[int] = ..., search: _Optional[bytes] = ..., bounds: _Optional[_Union[BoundsRequest, _Mapping]] = ..., sorting: _Optional[bytes] = ..., explain: bool = ..., custom_match: _Optional[bytes] = ...) -> None: ...

class BoundsRequest(_message.Message):
    __slots__ = ("match_keys", "type")
    MATCH_KEYS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    match_keys: bytes
    type: str
    def __init__(self, match_keys: _Optional[bytes] = ..., type: _Optional[str] = ...) -> None: ...

class ExtraInformation(_message.Message):
    __slots__ = ("bounds",)
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    bounds: bytes
    def __init__(self, bounds: _Optional[bytes] = ...) -> None: ...

class QueryExecutionStats(_message.Message):
    __slots__ = ("duration_ms", "docs_examined", "docs_returned", "cache_hit", "index_used", "database_type", "source_query_depth", "executed_at")
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    DOCS_EXAMINED_FIELD_NUMBER: _ClassVar[int]
    DOCS_RETURNED_FIELD_NUMBER: _ClassVar[int]
    CACHE_HIT_FIELD_NUMBER: _ClassVar[int]
    INDEX_USED_FIELD_NUMBER: _ClassVar[int]
    DATABASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_QUERY_DEPTH_FIELD_NUMBER: _ClassVar[int]
    EXECUTED_AT_FIELD_NUMBER: _ClassVar[int]
    duration_ms: int
    docs_examined: int
    docs_returned: int
    cache_hit: bool
    index_used: bool
    database_type: str
    source_query_depth: int
    executed_at: _timestamp_pb2.Timestamp
    def __init__(self, duration_ms: _Optional[int] = ..., docs_examined: _Optional[int] = ..., docs_returned: _Optional[int] = ..., cache_hit: bool = ..., index_used: bool = ..., database_type: _Optional[str] = ..., source_query_depth: _Optional[int] = ..., executed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AggregateResponse(_message.Message):
    __slots__ = ("data", "total", "total_sent", "next_page", "previous_page", "last_page", "extra_information", "stats")
    DATA_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SENT_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_PAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_PAGE_FIELD_NUMBER: _ClassVar[int]
    EXTRA_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    total: int
    total_sent: int
    next_page: int
    previous_page: int
    last_page: int
    extra_information: ExtraInformation
    stats: QueryExecutionStats
    def __init__(self, data: _Optional[bytes] = ..., total: _Optional[int] = ..., total_sent: _Optional[int] = ..., next_page: _Optional[int] = ..., previous_page: _Optional[int] = ..., last_page: _Optional[int] = ..., extra_information: _Optional[_Union[ExtraInformation, _Mapping]] = ..., stats: _Optional[_Union[QueryExecutionStats, _Mapping]] = ...) -> None: ...
