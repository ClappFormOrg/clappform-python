from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UsageRankBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USAGE_RANK_UNSPECIFIED: _ClassVar[UsageRankBy]
    USAGE_RANK_CALL_COUNT: _ClassVar[UsageRankBy]
    USAGE_RANK_AVG_DURATION_MS: _ClassVar[UsageRankBy]
    USAGE_RANK_TOTAL_DURATION_MS: _ClassVar[UsageRankBy]
    USAGE_RANK_UNIQUE_USERS: _ClassVar[UsageRankBy]
    USAGE_RANK_LAST_USED_DESC: _ClassVar[UsageRankBy]
    USAGE_RANK_LAST_USED_ASC: _ClassVar[UsageRankBy]
    USAGE_RANK_CACHE_MISS_RATE: _ClassVar[UsageRankBy]
USAGE_RANK_UNSPECIFIED: UsageRankBy
USAGE_RANK_CALL_COUNT: UsageRankBy
USAGE_RANK_AVG_DURATION_MS: UsageRankBy
USAGE_RANK_TOTAL_DURATION_MS: UsageRankBy
USAGE_RANK_UNIQUE_USERS: UsageRankBy
USAGE_RANK_LAST_USED_DESC: UsageRankBy
USAGE_RANK_LAST_USED_ASC: UsageRankBy
USAGE_RANK_CACHE_MISS_RATE: UsageRankBy

class QueryUsageRequest(_message.Message):
    __slots__ = ("query_id", "to")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    to: _timestamp_pb2.Timestamp
    def __init__(self, query_id: _Optional[str] = ..., to: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., **kwargs) -> None: ...

class CollectionUsageRequest(_message.Message):
    __slots__ = ("collection_id", "to")
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    collection_id: str
    to: _timestamp_pb2.Timestamp
    def __init__(self, collection_id: _Optional[str] = ..., to: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., **kwargs) -> None: ...

class TopUsageRequest(_message.Message):
    __slots__ = ("to", "limit", "rank_by", "min_call_count")
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    RANK_BY_FIELD_NUMBER: _ClassVar[int]
    MIN_CALL_COUNT_FIELD_NUMBER: _ClassVar[int]
    to: _timestamp_pb2.Timestamp
    limit: int
    rank_by: UsageRankBy
    min_call_count: int
    def __init__(self, to: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., limit: _Optional[int] = ..., rank_by: _Optional[_Union[UsageRankBy, str]] = ..., min_call_count: _Optional[int] = ..., **kwargs) -> None: ...

class UsageStat(_message.Message):
    __slots__ = ("query_id", "collection_id", "call_count", "unique_users", "avg_duration_ms", "total_duration_ms", "cache_hit_count", "cache_miss_rate", "total_rows_returned", "last_used", "first_used")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CALL_COUNT_FIELD_NUMBER: _ClassVar[int]
    UNIQUE_USERS_FIELD_NUMBER: _ClassVar[int]
    AVG_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    CACHE_HIT_COUNT_FIELD_NUMBER: _ClassVar[int]
    CACHE_MISS_RATE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ROWS_RETURNED_FIELD_NUMBER: _ClassVar[int]
    LAST_USED_FIELD_NUMBER: _ClassVar[int]
    FIRST_USED_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    collection_id: str
    call_count: int
    unique_users: int
    avg_duration_ms: float
    total_duration_ms: int
    cache_hit_count: int
    cache_miss_rate: float
    total_rows_returned: int
    last_used: _timestamp_pb2.Timestamp
    first_used: _timestamp_pb2.Timestamp
    def __init__(self, query_id: _Optional[str] = ..., collection_id: _Optional[str] = ..., call_count: _Optional[int] = ..., unique_users: _Optional[int] = ..., avg_duration_ms: _Optional[float] = ..., total_duration_ms: _Optional[int] = ..., cache_hit_count: _Optional[int] = ..., cache_miss_rate: _Optional[float] = ..., total_rows_returned: _Optional[int] = ..., last_used: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., first_used: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class QueryUsageResponse(_message.Message):
    __slots__ = ("stat",)
    STAT_FIELD_NUMBER: _ClassVar[int]
    stat: UsageStat
    def __init__(self, stat: _Optional[_Union[UsageStat, _Mapping]] = ...) -> None: ...

class CollectionUsageResponse(_message.Message):
    __slots__ = ("stat",)
    STAT_FIELD_NUMBER: _ClassVar[int]
    stat: UsageStat
    def __init__(self, stat: _Optional[_Union[UsageStat, _Mapping]] = ...) -> None: ...

class TopQueriesResponse(_message.Message):
    __slots__ = ("stats",)
    STATS_FIELD_NUMBER: _ClassVar[int]
    stats: _containers.RepeatedCompositeFieldContainer[UsageStat]
    def __init__(self, stats: _Optional[_Iterable[_Union[UsageStat, _Mapping]]] = ...) -> None: ...

class TopCollectionsResponse(_message.Message):
    __slots__ = ("stats",)
    STATS_FIELD_NUMBER: _ClassVar[int]
    stats: _containers.RepeatedCompositeFieldContainer[UsageStat]
    def __init__(self, stats: _Optional[_Iterable[_Union[UsageStat, _Mapping]]] = ...) -> None: ...
