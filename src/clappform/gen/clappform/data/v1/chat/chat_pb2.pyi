from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[ErrorCode]
    INVALID_ARGUMENT: _ClassVar[ErrorCode]
    PERMISSION_DENIED: _ClassVar[ErrorCode]
    CHAT_NOT_FOUND: _ClassVar[ErrorCode]
    MESSAGE_INVALID: _ClassVar[ErrorCode]
    INTERNAL_ERROR: _ClassVar[ErrorCode]
    RATE_LIMITED: _ClassVar[ErrorCode]
    UNAUTHORIZED: _ClassVar[ErrorCode]
    CONFLICT: _ClassVar[ErrorCode]
    ALREADY_EXISTS: _ClassVar[ErrorCode]
    MODEL_UNAVAILABLE: _ClassVar[ErrorCode]
    CHAT_LENGTH_LIMIT: _ClassVar[ErrorCode]
    RESOURCE_EXHAUSTED: _ClassVar[ErrorCode]

class NoticeCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOTICE_CODE_UNKNOWN: _ClassVar[NoticeCode]
    NOTICE_CODE_MODEL_MIGRATED: _ClassVar[NoticeCode]
    NOTICE_CODE_AI_QUERY_BUDGET_EXCEEDED: _ClassVar[NoticeCode]
    NOTICE_CODE_COST_CAP_SOFT: _ClassVar[NoticeCode]
    NOTICE_CODE_DATA_ACCESS_DENIED: _ClassVar[NoticeCode]
    NOTICE_CODE_INTENT_REWRITTEN: _ClassVar[NoticeCode]
    NOTICE_CODE_QUERY_EXECUTED: _ClassVar[NoticeCode]
    NOTICE_CODE_AIQUERY_FAILED: _ClassVar[NoticeCode]
    NOTICE_CODE_RESULT_TRUNCATED: _ClassVar[NoticeCode]
    NOTICE_CODE_FILTER_DROPPED: _ClassVar[NoticeCode]
    NOTICE_CODE_FK_LABEL_MISS: _ClassVar[NoticeCode]
    NOTICE_CODE_SCOPE_EXPANDED: _ClassVar[NoticeCode]
    NOTICE_CODE_AIQUERY_RETRY_HINT: _ClassVar[NoticeCode]
    NOTICE_CODE_FOLLOWUPS: _ClassVar[NoticeCode]
    NOTICE_CODE_DEEP_DIVE_BOUND: _ClassVar[NoticeCode]
    NOTICE_CODE_HINT_APPLIED: _ClassVar[NoticeCode]
    NOTICE_CODE_PROGRESS_AIQUERY_PLANNING: _ClassVar[NoticeCode]
    NOTICE_CODE_PROGRESS_AIQUERY_EXECUTING: _ClassVar[NoticeCode]
    NOTICE_CODE_PROGRESS_AIQUERY_DONE: _ClassVar[NoticeCode]
    NOTICE_CODE_PROGRESS_AIQUERY_SKIPPED: _ClassVar[NoticeCode]
    NOTICE_CODE_PROGRESS_GENERATING: _ClassVar[NoticeCode]
    NOTICE_CODE_PROGRESS_FIRST_TOKEN: _ClassVar[NoticeCode]

class QueryFailureReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUERY_FAILURE_REASON_UNSPECIFIED: _ClassVar[QueryFailureReason]
    QUERY_FAILURE_REASON_GENERATOR_ERROR: _ClassVar[QueryFailureReason]
    QUERY_FAILURE_REASON_VALIDATION_ERROR: _ClassVar[QueryFailureReason]
    QUERY_FAILURE_REASON_EXECUTION_ERROR: _ClassVar[QueryFailureReason]
    QUERY_FAILURE_REASON_SKIPPED: _ClassVar[QueryFailureReason]
    QUERY_FAILURE_REASON_BUDGET_EXCEEDED: _ClassVar[QueryFailureReason]
    QUERY_FAILURE_REASON_COMPILE_ERROR: _ClassVar[QueryFailureReason]
    QUERY_FAILURE_REASON_EMPTY_RESULT: _ClassVar[QueryFailureReason]
UNKNOWN: ErrorCode
INVALID_ARGUMENT: ErrorCode
PERMISSION_DENIED: ErrorCode
CHAT_NOT_FOUND: ErrorCode
MESSAGE_INVALID: ErrorCode
INTERNAL_ERROR: ErrorCode
RATE_LIMITED: ErrorCode
UNAUTHORIZED: ErrorCode
CONFLICT: ErrorCode
ALREADY_EXISTS: ErrorCode
MODEL_UNAVAILABLE: ErrorCode
CHAT_LENGTH_LIMIT: ErrorCode
RESOURCE_EXHAUSTED: ErrorCode
NOTICE_CODE_UNKNOWN: NoticeCode
NOTICE_CODE_MODEL_MIGRATED: NoticeCode
NOTICE_CODE_AI_QUERY_BUDGET_EXCEEDED: NoticeCode
NOTICE_CODE_COST_CAP_SOFT: NoticeCode
NOTICE_CODE_DATA_ACCESS_DENIED: NoticeCode
NOTICE_CODE_INTENT_REWRITTEN: NoticeCode
NOTICE_CODE_QUERY_EXECUTED: NoticeCode
NOTICE_CODE_AIQUERY_FAILED: NoticeCode
NOTICE_CODE_RESULT_TRUNCATED: NoticeCode
NOTICE_CODE_FILTER_DROPPED: NoticeCode
NOTICE_CODE_FK_LABEL_MISS: NoticeCode
NOTICE_CODE_SCOPE_EXPANDED: NoticeCode
NOTICE_CODE_AIQUERY_RETRY_HINT: NoticeCode
NOTICE_CODE_FOLLOWUPS: NoticeCode
NOTICE_CODE_DEEP_DIVE_BOUND: NoticeCode
NOTICE_CODE_HINT_APPLIED: NoticeCode
NOTICE_CODE_PROGRESS_AIQUERY_PLANNING: NoticeCode
NOTICE_CODE_PROGRESS_AIQUERY_EXECUTING: NoticeCode
NOTICE_CODE_PROGRESS_AIQUERY_DONE: NoticeCode
NOTICE_CODE_PROGRESS_AIQUERY_SKIPPED: NoticeCode
NOTICE_CODE_PROGRESS_GENERATING: NoticeCode
NOTICE_CODE_PROGRESS_FIRST_TOKEN: NoticeCode
QUERY_FAILURE_REASON_UNSPECIFIED: QueryFailureReason
QUERY_FAILURE_REASON_GENERATOR_ERROR: QueryFailureReason
QUERY_FAILURE_REASON_VALIDATION_ERROR: QueryFailureReason
QUERY_FAILURE_REASON_EXECUTION_ERROR: QueryFailureReason
QUERY_FAILURE_REASON_SKIPPED: QueryFailureReason
QUERY_FAILURE_REASON_BUDGET_EXCEEDED: QueryFailureReason
QUERY_FAILURE_REASON_COMPILE_ERROR: QueryFailureReason
QUERY_FAILURE_REASON_EMPTY_RESULT: QueryFailureReason

class Error(_message.Message):
    __slots__ = ("code", "message", "details")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    message: str
    details: str
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., message: _Optional[str] = ..., details: _Optional[str] = ...) -> None: ...

class Notice(_message.Message):
    __slots__ = ("code", "message", "is_progress", "intent_rewritten", "query_executed", "result_truncated", "filter_dropped", "fk_label_miss", "scope_expanded", "retry_hint", "followups", "deep_dive_bound")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IS_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    INTENT_REWRITTEN_FIELD_NUMBER: _ClassVar[int]
    QUERY_EXECUTED_FIELD_NUMBER: _ClassVar[int]
    RESULT_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    FILTER_DROPPED_FIELD_NUMBER: _ClassVar[int]
    FK_LABEL_MISS_FIELD_NUMBER: _ClassVar[int]
    SCOPE_EXPANDED_FIELD_NUMBER: _ClassVar[int]
    RETRY_HINT_FIELD_NUMBER: _ClassVar[int]
    FOLLOWUPS_FIELD_NUMBER: _ClassVar[int]
    DEEP_DIVE_BOUND_FIELD_NUMBER: _ClassVar[int]
    code: NoticeCode
    message: str
    is_progress: bool
    intent_rewritten: IntentRewritten
    query_executed: QueryExecuted
    result_truncated: ResultTruncated
    filter_dropped: FilterDropped
    fk_label_miss: FKLabelMiss
    scope_expanded: ScopeExpanded
    retry_hint: RetryHint
    followups: Followups
    deep_dive_bound: DeepDiveBound
    def __init__(self, code: _Optional[_Union[NoticeCode, str]] = ..., message: _Optional[str] = ..., is_progress: bool = ..., intent_rewritten: _Optional[_Union[IntentRewritten, _Mapping]] = ..., query_executed: _Optional[_Union[QueryExecuted, _Mapping]] = ..., result_truncated: _Optional[_Union[ResultTruncated, _Mapping]] = ..., filter_dropped: _Optional[_Union[FilterDropped, _Mapping]] = ..., fk_label_miss: _Optional[_Union[FKLabelMiss, _Mapping]] = ..., scope_expanded: _Optional[_Union[ScopeExpanded, _Mapping]] = ..., retry_hint: _Optional[_Union[RetryHint, _Mapping]] = ..., followups: _Optional[_Union[Followups, _Mapping]] = ..., deep_dive_bound: _Optional[_Union[DeepDiveBound, _Mapping]] = ...) -> None: ...

class IntentRewritten(_message.Message):
    __slots__ = ("data_intent", "rewritten_query", "classifier_model_id", "used_fast_path")
    DATA_INTENT_FIELD_NUMBER: _ClassVar[int]
    REWRITTEN_QUERY_FIELD_NUMBER: _ClassVar[int]
    CLASSIFIER_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    USED_FAST_PATH_FIELD_NUMBER: _ClassVar[int]
    data_intent: bool
    rewritten_query: str
    classifier_model_id: str
    used_fast_path: bool
    def __init__(self, data_intent: bool = ..., rewritten_query: _Optional[str] = ..., classifier_model_id: _Optional[str] = ..., used_fast_path: bool = ...) -> None: ...

class QueryExecuted(_message.Message):
    __slots__ = ("collection_id", "slug", "pipeline_json", "row_count", "status", "failure_reason", "failure_reason_code")
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_JSON_FIELD_NUMBER: _ClassVar[int]
    ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FAILURE_REASON_FIELD_NUMBER: _ClassVar[int]
    FAILURE_REASON_CODE_FIELD_NUMBER: _ClassVar[int]
    collection_id: str
    slug: str
    pipeline_json: str
    row_count: int
    status: str
    failure_reason: str
    failure_reason_code: QueryFailureReason
    def __init__(self, collection_id: _Optional[str] = ..., slug: _Optional[str] = ..., pipeline_json: _Optional[str] = ..., row_count: _Optional[int] = ..., status: _Optional[str] = ..., failure_reason: _Optional[str] = ..., failure_reason_code: _Optional[_Union[QueryFailureReason, str]] = ...) -> None: ...

class ResultTruncated(_message.Message):
    __slots__ = ("row_cap", "more_available")
    ROW_CAP_FIELD_NUMBER: _ClassVar[int]
    MORE_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    row_cap: int
    more_available: bool
    def __init__(self, row_cap: _Optional[int] = ..., more_available: bool = ...) -> None: ...

class FilterDropped(_message.Message):
    __slots__ = ("field", "op", "value", "reason")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    field: str
    op: str
    value: str
    reason: str
    def __init__(self, field: _Optional[str] = ..., op: _Optional[str] = ..., value: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class FKLabelMiss(_message.Message):
    __slots__ = ("related_collection_id", "related_slug", "unresolved_labels")
    RELATED_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    RELATED_SLUG_FIELD_NUMBER: _ClassVar[int]
    UNRESOLVED_LABELS_FIELD_NUMBER: _ClassVar[int]
    related_collection_id: str
    related_slug: str
    unresolved_labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, related_collection_id: _Optional[str] = ..., related_slug: _Optional[str] = ..., unresolved_labels: _Optional[_Iterable[str]] = ...) -> None: ...

class ScopeExpanded(_message.Message):
    __slots__ = ("requested_collection_ids", "effective_collection_ids", "trigger_permission")
    REQUESTED_COLLECTION_IDS_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_COLLECTION_IDS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_PERMISSION_FIELD_NUMBER: _ClassVar[int]
    requested_collection_ids: _containers.RepeatedScalarFieldContainer[str]
    effective_collection_ids: _containers.RepeatedScalarFieldContainer[str]
    trigger_permission: str
    def __init__(self, requested_collection_ids: _Optional[_Iterable[str]] = ..., effective_collection_ids: _Optional[_Iterable[str]] = ..., trigger_permission: _Optional[str] = ...) -> None: ...

class RetryHint(_message.Message):
    __slots__ = ("suggestions",)
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    suggestions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, suggestions: _Optional[_Iterable[str]] = ...) -> None: ...

class Followups(_message.Message):
    __slots__ = ("suggestions",)
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    suggestions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, suggestions: _Optional[_Iterable[str]] = ...) -> None: ...

class DeepDiveBound(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: _Optional[_Iterable[str]] = ...) -> None: ...

class Heartbeat(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StreamMessageResponse(_message.Message):
    __slots__ = ("message", "chat", "error", "notice", "heartbeat", "timestamp")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CHAT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NOTICE_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    message: Message
    chat: Chat
    error: Error
    notice: Notice
    heartbeat: Heartbeat
    timestamp: int
    def __init__(self, message: _Optional[_Union[Message, _Mapping]] = ..., chat: _Optional[_Union[Chat, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ..., notice: _Optional[_Union[Notice, _Mapping]] = ..., heartbeat: _Optional[_Union[Heartbeat, _Mapping]] = ..., timestamp: _Optional[int] = ...) -> None: ...

class SendMessageRequest(_message.Message):
    __slots__ = ("id", "payload")
    ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    id: str
    payload: SendMessageRequestPayload
    def __init__(self, id: _Optional[str] = ..., payload: _Optional[_Union[SendMessageRequestPayload, _Mapping]] = ...) -> None: ...

class SendMessageRequestPayload(_message.Message):
    __slots__ = ("content", "ai_collection_scopes", "context", "deep_dive")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    AI_COLLECTION_SCOPES_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    DEEP_DIVE_FIELD_NUMBER: _ClassVar[int]
    content: str
    ai_collection_scopes: _containers.RepeatedScalarFieldContainer[str]
    context: _containers.RepeatedCompositeFieldContainer[ContextItem]
    deep_dive: bytes
    def __init__(self, content: _Optional[str] = ..., ai_collection_scopes: _Optional[_Iterable[str]] = ..., context: _Optional[_Iterable[_Union[ContextItem, _Mapping]]] = ..., deep_dive: _Optional[bytes] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("id", "sender", "content", "timestamp", "chunk", "context")
    ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: str
    sender: str
    content: str
    timestamp: int
    chunk: int
    context: _containers.RepeatedCompositeFieldContainer[ContextItem]
    def __init__(self, id: _Optional[str] = ..., sender: _Optional[str] = ..., content: _Optional[str] = ..., timestamp: _Optional[int] = ..., chunk: _Optional[int] = ..., context: _Optional[_Iterable[_Union[ContextItem, _Mapping]]] = ...) -> None: ...

class Widget(_message.Message):
    __slots__ = ("id", "name", "queries", "data", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    queries: _containers.RepeatedScalarFieldContainer[str]
    data: str
    type: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., queries: _Optional[_Iterable[str]] = ..., data: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ("id", "name", "metadata_collection")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    metadata_collection: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., metadata_collection: _Optional[str] = ...) -> None: ...

class Collection(_message.Message):
    __slots__ = ("id", "slug", "files")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    id: str
    slug: str
    files: _containers.RepeatedCompositeFieldContainer[File]
    def __init__(self, id: _Optional[str] = ..., slug: _Optional[str] = ..., files: _Optional[_Iterable[_Union[File, _Mapping]]] = ...) -> None: ...

class ContextItem(_message.Message):
    __slots__ = ("widget", "collection")
    WIDGET_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    widget: Widget
    collection: Collection
    def __init__(self, widget: _Optional[_Union[Widget, _Mapping]] = ..., collection: _Optional[_Union[Collection, _Mapping]] = ...) -> None: ...

class Messages(_message.Message):
    __slots__ = ("messages", "cursor")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[Message]
    cursor: int
    def __init__(self, messages: _Optional[_Iterable[_Union[Message, _Mapping]]] = ..., cursor: _Optional[int] = ...) -> None: ...

class Chat(_message.Message):
    __slots__ = ("id", "name", "model_id", "fallback_model_id", "name_auto_generated", "keep_in_memory", "archived_at", "created_at", "updated_at", "settings", "default_collection_scopes")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_AUTO_GENERATED_FIELD_NUMBER: _ClassVar[int]
    KEEP_IN_MEMORY_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_COLLECTION_SCOPES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    model_id: str
    fallback_model_id: str
    name_auto_generated: bool
    keep_in_memory: bool
    archived_at: int
    created_at: int
    updated_at: int
    settings: ChatSettings
    default_collection_scopes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., model_id: _Optional[str] = ..., fallback_model_id: _Optional[str] = ..., name_auto_generated: bool = ..., keep_in_memory: bool = ..., archived_at: _Optional[int] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., settings: _Optional[_Union[ChatSettings, _Mapping]] = ..., default_collection_scopes: _Optional[_Iterable[str]] = ...) -> None: ...

class ChatSettings(_message.Message):
    __slots__ = ("inherit", "locale", "name", "occupation", "traits", "max_row_limit", "max_group_limit")
    INHERIT_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OCCUPATION_FIELD_NUMBER: _ClassVar[int]
    TRAITS_FIELD_NUMBER: _ClassVar[int]
    MAX_ROW_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MAX_GROUP_LIMIT_FIELD_NUMBER: _ClassVar[int]
    inherit: bool
    locale: str
    name: str
    occupation: str
    traits: str
    max_row_limit: int
    max_group_limit: int
    def __init__(self, inherit: bool = ..., locale: _Optional[str] = ..., name: _Optional[str] = ..., occupation: _Optional[str] = ..., traits: _Optional[str] = ..., max_row_limit: _Optional[int] = ..., max_group_limit: _Optional[int] = ...) -> None: ...

class Chats(_message.Message):
    __slots__ = ("chats",)
    CHATS_FIELD_NUMBER: _ClassVar[int]
    chats: _containers.RepeatedCompositeFieldContainer[Chat]
    def __init__(self, chats: _Optional[_Iterable[_Union[Chat, _Mapping]]] = ...) -> None: ...

class GetChatsRequest(_message.Message):
    __slots__ = ("app_id",)
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    def __init__(self, app_id: _Optional[str] = ...) -> None: ...

class GetChatRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetMessagesRequest(_message.Message):
    __slots__ = ("id", "cursor")
    ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    cursor: int
    def __init__(self, id: _Optional[str] = ..., cursor: _Optional[int] = ...) -> None: ...

class CreateChatRequest(_message.Message):
    __slots__ = ("app_id", "model_id", "settings", "default_collection_scopes", "keep_in_memory")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_COLLECTION_SCOPES_FIELD_NUMBER: _ClassVar[int]
    KEEP_IN_MEMORY_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    model_id: str
    settings: ChatSettings
    default_collection_scopes: _containers.RepeatedScalarFieldContainer[str]
    keep_in_memory: bool
    def __init__(self, app_id: _Optional[str] = ..., model_id: _Optional[str] = ..., settings: _Optional[_Union[ChatSettings, _Mapping]] = ..., default_collection_scopes: _Optional[_Iterable[str]] = ..., keep_in_memory: bool = ...) -> None: ...

class UpdateChatRequest(_message.Message):
    __slots__ = ("id", "chat")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_FIELD_NUMBER: _ClassVar[int]
    id: str
    chat: ChatUpdate
    def __init__(self, id: _Optional[str] = ..., chat: _Optional[_Union[ChatUpdate, _Mapping]] = ...) -> None: ...

class ChatUpdate(_message.Message):
    __slots__ = ("name", "settings", "default_collection_scopes")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_COLLECTION_SCOPES_FIELD_NUMBER: _ClassVar[int]
    name: str
    settings: ChatSettings
    default_collection_scopes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., settings: _Optional[_Union[ChatSettings, _Mapping]] = ..., default_collection_scopes: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteChatRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SetKeepInMemoryRequest(_message.Message):
    __slots__ = ("id", "keep_in_memory")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEEP_IN_MEMORY_FIELD_NUMBER: _ClassVar[int]
    id: str
    keep_in_memory: bool
    def __init__(self, id: _Optional[str] = ..., keep_in_memory: bool = ...) -> None: ...

class RefreshSchemaCacheRequest(_message.Message):
    __slots__ = ("app_id", "collection_id")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    collection_id: str
    def __init__(self, app_id: _Optional[str] = ..., collection_id: _Optional[str] = ...) -> None: ...

class BuildQueryRequest(_message.Message):
    __slots__ = ("prompt", "collection_ids", "model_id")
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_IDS_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    collection_ids: _containers.RepeatedScalarFieldContainer[str]
    model_id: str
    def __init__(self, prompt: _Optional[str] = ..., collection_ids: _Optional[_Iterable[str]] = ..., model_id: _Optional[str] = ...) -> None: ...

class BuildQueryResponse(_message.Message):
    __slots__ = ("skipped", "skip_reason", "plan", "dropped_collection_ids", "resolved_model_id")
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    SKIP_REASON_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    DROPPED_COLLECTION_IDS_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    skipped: bool
    skip_reason: str
    plan: bytes
    dropped_collection_ids: _containers.RepeatedScalarFieldContainer[str]
    resolved_model_id: str
    def __init__(self, skipped: bool = ..., skip_reason: _Optional[str] = ..., plan: _Optional[bytes] = ..., dropped_collection_ids: _Optional[_Iterable[str]] = ..., resolved_model_id: _Optional[str] = ...) -> None: ...
