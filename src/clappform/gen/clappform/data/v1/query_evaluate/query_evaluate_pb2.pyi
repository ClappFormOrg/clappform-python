from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EvaluateQueryRequest(_message.Message):
    __slots__ = ("query_id", "model_id")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    model_id: str
    def __init__(self, query_id: _Optional[str] = ..., model_id: _Optional[str] = ...) -> None: ...

class EvaluateQueryResponse(_message.Message):
    __slots__ = ("evaluation", "from_cache")
    EVALUATION_FIELD_NUMBER: _ClassVar[int]
    FROM_CACHE_FIELD_NUMBER: _ClassVar[int]
    evaluation: QueryEvaluationProto
    from_cache: bool
    def __init__(self, evaluation: _Optional[_Union[QueryEvaluationProto, _Mapping]] = ..., from_cache: bool = ...) -> None: ...

class EvaluateCollectionRequest(_message.Message):
    __slots__ = ("collection_id", "model_id", "force_refresh")
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    FORCE_REFRESH_FIELD_NUMBER: _ClassVar[int]
    collection_id: str
    model_id: str
    force_refresh: bool
    def __init__(self, collection_id: _Optional[str] = ..., model_id: _Optional[str] = ..., force_refresh: bool = ...) -> None: ...

class EvaluateCollectionResponse(_message.Message):
    __slots__ = ("evaluations", "failed", "summary")
    EVALUATIONS_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    evaluations: _containers.RepeatedCompositeFieldContainer[QueryEvaluationProto]
    failed: _containers.RepeatedCompositeFieldContainer[FailedEvaluationProto]
    summary: EvaluationSummaryProto
    def __init__(self, evaluations: _Optional[_Iterable[_Union[QueryEvaluationProto, _Mapping]]] = ..., failed: _Optional[_Iterable[_Union[FailedEvaluationProto, _Mapping]]] = ..., summary: _Optional[_Union[EvaluationSummaryProto, _Mapping]] = ...) -> None: ...

class EvaluateAppRequest(_message.Message):
    __slots__ = ("app_id", "model_id", "force_refresh")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    FORCE_REFRESH_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    model_id: str
    force_refresh: bool
    def __init__(self, app_id: _Optional[str] = ..., model_id: _Optional[str] = ..., force_refresh: bool = ...) -> None: ...

class EvaluateAppResponse(_message.Message):
    __slots__ = ("evaluations", "failed", "summary", "dropped_collection_ids", "skipped_query_ids")
    EVALUATIONS_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    DROPPED_COLLECTION_IDS_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_QUERY_IDS_FIELD_NUMBER: _ClassVar[int]
    evaluations: _containers.RepeatedCompositeFieldContainer[QueryEvaluationProto]
    failed: _containers.RepeatedCompositeFieldContainer[FailedEvaluationProto]
    summary: EvaluationSummaryProto
    dropped_collection_ids: _containers.RepeatedScalarFieldContainer[str]
    skipped_query_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, evaluations: _Optional[_Iterable[_Union[QueryEvaluationProto, _Mapping]]] = ..., failed: _Optional[_Iterable[_Union[FailedEvaluationProto, _Mapping]]] = ..., summary: _Optional[_Union[EvaluationSummaryProto, _Mapping]] = ..., dropped_collection_ids: _Optional[_Iterable[str]] = ..., skipped_query_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetEvaluationRequest(_message.Message):
    __slots__ = ("query_id",)
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    def __init__(self, query_id: _Optional[str] = ...) -> None: ...

class GetEvaluationResponse(_message.Message):
    __slots__ = ("evaluation",)
    EVALUATION_FIELD_NUMBER: _ClassVar[int]
    evaluation: QueryEvaluationProto
    def __init__(self, evaluation: _Optional[_Union[QueryEvaluationProto, _Mapping]] = ...) -> None: ...

class QueryEvaluationProto(_message.Message):
    __slots__ = ("query_id", "collection_id", "app_id", "generated_at", "pipeline_hash", "explain_available", "explain_stats", "suggestions", "skip_reason", "model_id", "importance_score")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_HASH_FIELD_NUMBER: _ClassVar[int]
    EXPLAIN_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    EXPLAIN_STATS_FIELD_NUMBER: _ClassVar[int]
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    SKIP_REASON_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    IMPORTANCE_SCORE_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    collection_id: str
    app_id: str
    generated_at: int
    pipeline_hash: str
    explain_available: bool
    explain_stats: ExplainStatsProto
    suggestions: _containers.RepeatedCompositeFieldContainer[SuggestionProto]
    skip_reason: str
    model_id: str
    importance_score: float
    def __init__(self, query_id: _Optional[str] = ..., collection_id: _Optional[str] = ..., app_id: _Optional[str] = ..., generated_at: _Optional[int] = ..., pipeline_hash: _Optional[str] = ..., explain_available: bool = ..., explain_stats: _Optional[_Union[ExplainStatsProto, _Mapping]] = ..., suggestions: _Optional[_Iterable[_Union[SuggestionProto, _Mapping]]] = ..., skip_reason: _Optional[str] = ..., model_id: _Optional[str] = ..., importance_score: _Optional[float] = ...) -> None: ...

class ExplainStatsProto(_message.Message):
    __slots__ = ("execution_time_millis", "n_returned", "n_scanned", "indexes_used", "stage")
    EXECUTION_TIME_MILLIS_FIELD_NUMBER: _ClassVar[int]
    N_RETURNED_FIELD_NUMBER: _ClassVar[int]
    N_SCANNED_FIELD_NUMBER: _ClassVar[int]
    INDEXES_USED_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    execution_time_millis: int
    n_returned: int
    n_scanned: int
    indexes_used: _containers.RepeatedScalarFieldContainer[str]
    stage: str
    def __init__(self, execution_time_millis: _Optional[int] = ..., n_returned: _Optional[int] = ..., n_scanned: _Optional[int] = ..., indexes_used: _Optional[_Iterable[str]] = ..., stage: _Optional[str] = ...) -> None: ...

class SuggestionProto(_message.Message):
    __slots__ = ("severity", "category", "stage_index", "field", "advice")
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    STAGE_INDEX_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    ADVICE_FIELD_NUMBER: _ClassVar[int]
    severity: str
    category: str
    stage_index: int
    field: str
    advice: str
    def __init__(self, severity: _Optional[str] = ..., category: _Optional[str] = ..., stage_index: _Optional[int] = ..., field: _Optional[str] = ..., advice: _Optional[str] = ...) -> None: ...

class FailedEvaluationProto(_message.Message):
    __slots__ = ("query_id", "reason")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    reason: str
    def __init__(self, query_id: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class EvaluationSummaryProto(_message.Message):
    __slots__ = ("evaluated", "cached", "failed", "skipped", "total_importance_score_evaluated", "total_importance_score_skipped")
    EVALUATED_FIELD_NUMBER: _ClassVar[int]
    CACHED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_IMPORTANCE_SCORE_EVALUATED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_IMPORTANCE_SCORE_SKIPPED_FIELD_NUMBER: _ClassVar[int]
    evaluated: int
    cached: int
    failed: int
    skipped: int
    total_importance_score_evaluated: float
    total_importance_score_skipped: float
    def __init__(self, evaluated: _Optional[int] = ..., cached: _Optional[int] = ..., failed: _Optional[int] = ..., skipped: _Optional[int] = ..., total_importance_score_evaluated: _Optional[float] = ..., total_importance_score_skipped: _Optional[float] = ...) -> None: ...
