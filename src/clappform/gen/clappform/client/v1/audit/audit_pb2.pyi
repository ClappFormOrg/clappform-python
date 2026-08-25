from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Error(_message.Message):
    __slots__ = ("code", "message", "type", "reason")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    type: str
    reason: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ..., type: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class RequestInfo(_message.Message):
    __slots__ = ("id", "method", "url", "elapsed", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    method: str
    url: str
    elapsed: int
    status: int
    def __init__(self, id: _Optional[str] = ..., method: _Optional[str] = ..., url: _Optional[str] = ..., elapsed: _Optional[int] = ..., status: _Optional[int] = ...) -> None: ...

class Log(_message.Message):
    __slots__ = ("id", "timestamp", "host", "level", "message", "location", "request", "error", "data")
    class DataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    timestamp: str
    host: str
    level: str
    message: str
    location: str
    request: RequestInfo
    error: Error
    data: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., timestamp: _Optional[str] = ..., host: _Optional[str] = ..., level: _Optional[str] = ..., message: _Optional[str] = ..., location: _Optional[str] = ..., request: _Optional[_Union[RequestInfo, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ..., data: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Logs(_message.Message):
    __slots__ = ("items", "total", "pagination")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[Log]
    total: int
    pagination: _commons_pb2.Pagination
    def __init__(self, items: _Optional[_Iterable[_Union[Log, _Mapping]]] = ..., total: _Optional[int] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AuditListRequest(_message.Message):
    __slots__ = ("pagination", "start_date", "end_date", "user_id", "request_id", "message", "level", "method", "method_prefix", "data_filters", "url", "url_prefix")
    class DataFiltersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    METHOD_PREFIX_FIELD_NUMBER: _ClassVar[int]
    DATA_FILTERS_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    URL_PREFIX_FIELD_NUMBER: _ClassVar[int]
    pagination: _commons_pb2.PaginationRequest
    start_date: int
    end_date: int
    user_id: str
    request_id: str
    message: str
    level: str
    method: str
    method_prefix: str
    data_filters: _containers.ScalarMap[str, str]
    url: str
    url_prefix: str
    def __init__(self, pagination: _Optional[_Union[_commons_pb2.PaginationRequest, _Mapping]] = ..., start_date: _Optional[int] = ..., end_date: _Optional[int] = ..., user_id: _Optional[str] = ..., request_id: _Optional[str] = ..., message: _Optional[str] = ..., level: _Optional[str] = ..., method: _Optional[str] = ..., method_prefix: _Optional[str] = ..., data_filters: _Optional[_Mapping[str, str]] = ..., url: _Optional[str] = ..., url_prefix: _Optional[str] = ...) -> None: ...

class TimeRangeRequest(_message.Message):
    __slots__ = ("start_date", "end_date")
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    start_date: int
    end_date: int
    def __init__(self, start_date: _Optional[int] = ..., end_date: _Optional[int] = ...) -> None: ...

class TimeSeriesPoint(_message.Message):
    __slots__ = ("timestamp", "count", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    count: int
    value: float
    def __init__(self, timestamp: _Optional[str] = ..., count: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...

class UsageMetric(_message.Message):
    __slots__ = ("name", "count", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    count: int
    value: float
    def __init__(self, name: _Optional[str] = ..., count: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...

class APIUsageStats(_message.Message):
    __slots__ = ("time_series_data", "top_endpoints", "method_stats", "status_code_stats", "avg_response_time_ms")
    TIME_SERIES_DATA_FIELD_NUMBER: _ClassVar[int]
    TOP_ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    METHOD_STATS_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_STATS_FIELD_NUMBER: _ClassVar[int]
    AVG_RESPONSE_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    time_series_data: _containers.RepeatedCompositeFieldContainer[TimeSeriesPoint]
    top_endpoints: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    method_stats: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    status_code_stats: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    avg_response_time_ms: float
    def __init__(self, time_series_data: _Optional[_Iterable[_Union[TimeSeriesPoint, _Mapping]]] = ..., top_endpoints: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., method_stats: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., status_code_stats: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., avg_response_time_ms: _Optional[float] = ...) -> None: ...

class ErrorStats(_message.Message):
    __slots__ = ("error_types", "error_codes", "time_series_data")
    ERROR_TYPES_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODES_FIELD_NUMBER: _ClassVar[int]
    TIME_SERIES_DATA_FIELD_NUMBER: _ClassVar[int]
    error_types: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    error_codes: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    time_series_data: _containers.RepeatedCompositeFieldContainer[TimeSeriesPoint]
    def __init__(self, error_types: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., error_codes: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., time_series_data: _Optional[_Iterable[_Union[TimeSeriesPoint, _Mapping]]] = ...) -> None: ...

class UserActivityStats(_message.Message):
    __slots__ = ("active_users", "activity_by_hour", "user_error_rates", "avg_session_duration_sec")
    ACTIVE_USERS_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_BY_HOUR_FIELD_NUMBER: _ClassVar[int]
    USER_ERROR_RATES_FIELD_NUMBER: _ClassVar[int]
    AVG_SESSION_DURATION_SEC_FIELD_NUMBER: _ClassVar[int]
    active_users: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    activity_by_hour: _containers.RepeatedCompositeFieldContainer[TimeSeriesPoint]
    user_error_rates: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    avg_session_duration_sec: float
    def __init__(self, active_users: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., activity_by_hour: _Optional[_Iterable[_Union[TimeSeriesPoint, _Mapping]]] = ..., user_error_rates: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., avg_session_duration_sec: _Optional[float] = ...) -> None: ...

class PerformanceStats(_message.Message):
    __slots__ = ("endpoint_latencies", "peak_times", "slow_endpoints", "p95_response_time_ms", "p99_response_time_ms", "slow_http_endpoints")
    ENDPOINT_LATENCIES_FIELD_NUMBER: _ClassVar[int]
    PEAK_TIMES_FIELD_NUMBER: _ClassVar[int]
    SLOW_ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    P95_RESPONSE_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    P99_RESPONSE_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    SLOW_HTTP_ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    endpoint_latencies: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    peak_times: _containers.RepeatedCompositeFieldContainer[TimeSeriesPoint]
    slow_endpoints: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    p95_response_time_ms: float
    p99_response_time_ms: float
    slow_http_endpoints: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    def __init__(self, endpoint_latencies: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., peak_times: _Optional[_Iterable[_Union[TimeSeriesPoint, _Mapping]]] = ..., slow_endpoints: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., p95_response_time_ms: _Optional[float] = ..., p99_response_time_ms: _Optional[float] = ..., slow_http_endpoints: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ...) -> None: ...

class SecurityStats(_message.Message):
    __slots__ = ("failed_auth_by_ip", "auth_failures", "unusual_activity", "total_failed_attempts")
    FAILED_AUTH_BY_IP_FIELD_NUMBER: _ClassVar[int]
    AUTH_FAILURES_FIELD_NUMBER: _ClassVar[int]
    UNUSUAL_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FAILED_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    failed_auth_by_ip: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    auth_failures: _containers.RepeatedCompositeFieldContainer[TimeSeriesPoint]
    unusual_activity: _containers.RepeatedCompositeFieldContainer[UsageMetric]
    total_failed_attempts: int
    def __init__(self, failed_auth_by_ip: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., auth_failures: _Optional[_Iterable[_Union[TimeSeriesPoint, _Mapping]]] = ..., unusual_activity: _Optional[_Iterable[_Union[UsageMetric, _Mapping]]] = ..., total_failed_attempts: _Optional[int] = ...) -> None: ...
