from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RuleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RULE_TYPE_UNSPECIFIED: _ClassVar[RuleType]
    RULE_TYPE_SHARED: _ClassVar[RuleType]
    RULE_TYPE_CUSTOM: _ClassVar[RuleType]

class ConditionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONDITION_TYPE_UNSPECIFIED: _ClassVar[ConditionType]
    CONDITION_TYPE_MATCH: _ClassVar[ConditionType]
    CONDITION_TYPE_AGGREGATE_THRESHOLD: _ClassVar[ConditionType]
    CONDITION_TYPE_ABSENCE: _ClassVar[ConditionType]

class RecipientStrategy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RECIPIENT_STRATEGY_UNSPECIFIED: _ClassVar[RecipientStrategy]
    RECIPIENT_STRATEGY_FIELD_LOOKUP: _ClassVar[RecipientStrategy]
    RECIPIENT_STRATEGY_RELATED_LOOKUP: _ClassVar[RecipientStrategy]
    RECIPIENT_STRATEGY_STATIC_LIST: _ClassVar[RecipientStrategy]

class ExecutionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXECUTION_STATUS_UNSPECIFIED: _ClassVar[ExecutionStatus]
    EXECUTION_STATUS_DISPATCHING: _ClassVar[ExecutionStatus]
    EXECUTION_STATUS_SENT: _ClassVar[ExecutionStatus]
    EXECUTION_STATUS_FAILED: _ClassVar[ExecutionStatus]
    EXECUTION_STATUS_NO_RECIPIENTS: _ClassVar[ExecutionStatus]
    EXECUTION_STATUS_CONDITION_NOT_MATCHED: _ClassVar[ExecutionStatus]
RULE_TYPE_UNSPECIFIED: RuleType
RULE_TYPE_SHARED: RuleType
RULE_TYPE_CUSTOM: RuleType
CONDITION_TYPE_UNSPECIFIED: ConditionType
CONDITION_TYPE_MATCH: ConditionType
CONDITION_TYPE_AGGREGATE_THRESHOLD: ConditionType
CONDITION_TYPE_ABSENCE: ConditionType
RECIPIENT_STRATEGY_UNSPECIFIED: RecipientStrategy
RECIPIENT_STRATEGY_FIELD_LOOKUP: RecipientStrategy
RECIPIENT_STRATEGY_RELATED_LOOKUP: RecipientStrategy
RECIPIENT_STRATEGY_STATIC_LIST: RecipientStrategy
EXECUTION_STATUS_UNSPECIFIED: ExecutionStatus
EXECUTION_STATUS_DISPATCHING: ExecutionStatus
EXECUTION_STATUS_SENT: ExecutionStatus
EXECUTION_STATUS_FAILED: ExecutionStatus
EXECUTION_STATUS_NO_RECIPIENTS: ExecutionStatus
EXECUTION_STATUS_CONDITION_NOT_MATCHED: ExecutionStatus

class Rule(_message.Message):
    __slots__ = ("id", "rule_type", "name", "created_by", "enabled", "source_collection_id", "conditions", "recipient_strategy", "recipient_config", "notification_config", "schedule", "cooldown_minutes", "max_notifications", "created_at", "updated_at", "deleted_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    RULE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    SOURCE_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    COOLDOWN_MINUTES_FIELD_NUMBER: _ClassVar[int]
    MAX_NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    rule_type: RuleType
    name: str
    created_by: str
    enabled: bool
    source_collection_id: str
    conditions: Conditions
    recipient_strategy: RecipientStrategy
    recipient_config: RecipientConfig
    notification_config: NotificationConfig
    schedule: str
    cooldown_minutes: int
    max_notifications: int
    created_at: int
    updated_at: int
    deleted_at: int
    def __init__(self, id: _Optional[str] = ..., rule_type: _Optional[_Union[RuleType, str]] = ..., name: _Optional[str] = ..., created_by: _Optional[str] = ..., enabled: bool = ..., source_collection_id: _Optional[str] = ..., conditions: _Optional[_Union[Conditions, _Mapping]] = ..., recipient_strategy: _Optional[_Union[RecipientStrategy, str]] = ..., recipient_config: _Optional[_Union[RecipientConfig, _Mapping]] = ..., notification_config: _Optional[_Union[NotificationConfig, _Mapping]] = ..., schedule: _Optional[str] = ..., cooldown_minutes: _Optional[int] = ..., max_notifications: _Optional[int] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., deleted_at: _Optional[int] = ...) -> None: ...

class Conditions(_message.Message):
    __slots__ = ("type", "operator", "clauses", "group_by", "aggregate_field", "aggregate_op", "threshold_op", "threshold_value", "filter", "watch_field", "absence_window")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    CLAUSES_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_FIELD_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_OP_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_OP_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    WATCH_FIELD_FIELD_NUMBER: _ClassVar[int]
    ABSENCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    type: ConditionType
    operator: str
    clauses: _containers.RepeatedCompositeFieldContainer[Clause]
    group_by: str
    aggregate_field: str
    aggregate_op: str
    threshold_op: str
    threshold_value: float
    filter: Filter
    watch_field: str
    absence_window: str
    def __init__(self, type: _Optional[_Union[ConditionType, str]] = ..., operator: _Optional[str] = ..., clauses: _Optional[_Iterable[_Union[Clause, _Mapping]]] = ..., group_by: _Optional[str] = ..., aggregate_field: _Optional[str] = ..., aggregate_op: _Optional[str] = ..., threshold_op: _Optional[str] = ..., threshold_value: _Optional[float] = ..., filter: _Optional[_Union[Filter, _Mapping]] = ..., watch_field: _Optional[str] = ..., absence_window: _Optional[str] = ...) -> None: ...

class Clause(_message.Message):
    __slots__ = ("field", "op", "value")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    field: str
    op: str
    value: bytes
    def __init__(self, field: _Optional[str] = ..., op: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...

class Filter(_message.Message):
    __slots__ = ("operator", "clauses")
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    CLAUSES_FIELD_NUMBER: _ClassVar[int]
    operator: str
    clauses: _containers.RepeatedCompositeFieldContainer[Clause]
    def __init__(self, operator: _Optional[str] = ..., clauses: _Optional[_Iterable[_Union[Clause, _Mapping]]] = ...) -> None: ...

class RecipientConfig(_message.Message):
    __slots__ = ("descriptor_key", "field_key", "email_field", "first_name_field", "last_name_field", "recipients")
    DESCRIPTOR_KEY_FIELD_NUMBER: _ClassVar[int]
    FIELD_KEY_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_FIELD_NUMBER: _ClassVar[int]
    descriptor_key: str
    field_key: str
    email_field: str
    first_name_field: str
    last_name_field: str
    recipients: _containers.RepeatedCompositeFieldContainer[Recipient]
    def __init__(self, descriptor_key: _Optional[str] = ..., field_key: _Optional[str] = ..., email_field: _Optional[str] = ..., first_name_field: _Optional[str] = ..., last_name_field: _Optional[str] = ..., recipients: _Optional[_Iterable[_Union[Recipient, _Mapping]]] = ...) -> None: ...

class Recipient(_message.Message):
    __slots__ = ("email", "first_name", "last_name", "user_id")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    first_name: str
    last_name: str
    user_id: str
    def __init__(self, email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class NotificationConfig(_message.Message):
    __slots__ = ("channel", "subject", "body", "priority", "is_html")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    IS_HTML_FIELD_NUMBER: _ClassVar[int]
    channel: str
    subject: str
    body: str
    priority: str
    is_html: bool
    def __init__(self, channel: _Optional[str] = ..., subject: _Optional[str] = ..., body: _Optional[str] = ..., priority: _Optional[str] = ..., is_html: bool = ...) -> None: ...

class CreateRuleRequest(_message.Message):
    __slots__ = ("rule",)
    RULE_FIELD_NUMBER: _ClassVar[int]
    rule: Rule
    def __init__(self, rule: _Optional[_Union[Rule, _Mapping]] = ...) -> None: ...

class UpdateRuleRequest(_message.Message):
    __slots__ = ("rule",)
    RULE_FIELD_NUMBER: _ClassVar[int]
    rule: Rule
    def __init__(self, rule: _Optional[_Union[Rule, _Mapping]] = ...) -> None: ...

class DeleteRuleRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetRuleRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ListRulesRequest(_message.Message):
    __slots__ = ("source_collection_id", "rule_type", "enabled", "include_deleted", "page", "batch_size")
    SOURCE_COLLECTION_ID_FIELD_NUMBER: _ClassVar[int]
    RULE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    source_collection_id: str
    rule_type: RuleType
    enabled: bool
    include_deleted: bool
    page: int
    batch_size: int
    def __init__(self, source_collection_id: _Optional[str] = ..., rule_type: _Optional[_Union[RuleType, str]] = ..., enabled: bool = ..., include_deleted: bool = ..., page: _Optional[int] = ..., batch_size: _Optional[int] = ...) -> None: ...

class ListRulesResponse(_message.Message):
    __slots__ = ("rules", "total")
    RULES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[Rule]
    total: int
    def __init__(self, rules: _Optional[_Iterable[_Union[Rule, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class PreviewRuleRequest(_message.Message):
    __slots__ = ("rule",)
    RULE_FIELD_NUMBER: _ClassVar[int]
    rule: Rule
    def __init__(self, rule: _Optional[_Union[Rule, _Mapping]] = ...) -> None: ...

class PreviewRuleResponse(_message.Message):
    __slots__ = ("matched_count", "sample_docs", "recipient_count", "recipients_dropped", "rendered_subject", "rendered_body", "validation_warnings")
    MATCHED_COUNT_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_DOCS_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_DROPPED_FIELD_NUMBER: _ClassVar[int]
    RENDERED_SUBJECT_FIELD_NUMBER: _ClassVar[int]
    RENDERED_BODY_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_WARNINGS_FIELD_NUMBER: _ClassVar[int]
    matched_count: int
    sample_docs: _containers.RepeatedScalarFieldContainer[bytes]
    recipient_count: int
    recipients_dropped: int
    rendered_subject: str
    rendered_body: str
    validation_warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, matched_count: _Optional[int] = ..., sample_docs: _Optional[_Iterable[bytes]] = ..., recipient_count: _Optional[int] = ..., recipients_dropped: _Optional[int] = ..., rendered_subject: _Optional[str] = ..., rendered_body: _Optional[str] = ..., validation_warnings: _Optional[_Iterable[str]] = ...) -> None: ...

class TestFireRuleRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TestFireRuleResponse(_message.Message):
    __slots__ = ("condition_matched", "matched_count", "batch_id", "error")
    CONDITION_MATCHED_FIELD_NUMBER: _ClassVar[int]
    MATCHED_COUNT_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    condition_matched: bool
    matched_count: int
    batch_id: str
    error: str
    def __init__(self, condition_matched: bool = ..., matched_count: _Optional[int] = ..., batch_id: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class ListRuleExecutionsRequest(_message.Message):
    __slots__ = ("rule_id", "page", "batch_size")
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    rule_id: str
    page: int
    batch_size: int
    def __init__(self, rule_id: _Optional[str] = ..., page: _Optional[int] = ..., batch_size: _Optional[int] = ...) -> None: ...

class ListRuleExecutionsResponse(_message.Message):
    __slots__ = ("executions", "total")
    EXECUTIONS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    executions: _containers.RepeatedCompositeFieldContainer[ExecutionLog]
    total: int
    def __init__(self, executions: _Optional[_Iterable[_Union[ExecutionLog, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class ExecutionLog(_message.Message):
    __slots__ = ("id", "rule_id", "rule_name", "evaluated_at", "duration_ms", "condition_matched", "matched_count", "recipients_resolved", "recipients_notified", "recipients_dropped", "notification_sent", "group_value", "error", "batch_id", "is_test", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    RULE_ID_FIELD_NUMBER: _ClassVar[int]
    RULE_NAME_FIELD_NUMBER: _ClassVar[int]
    EVALUATED_AT_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    CONDITION_MATCHED_FIELD_NUMBER: _ClassVar[int]
    MATCHED_COUNT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_RESOLVED_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_NOTIFIED_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_DROPPED_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_SENT_FIELD_NUMBER: _ClassVar[int]
    GROUP_VALUE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    IS_TEST_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    rule_id: str
    rule_name: str
    evaluated_at: int
    duration_ms: int
    condition_matched: bool
    matched_count: int
    recipients_resolved: int
    recipients_notified: int
    recipients_dropped: int
    notification_sent: bool
    group_value: str
    error: str
    batch_id: str
    is_test: bool
    status: ExecutionStatus
    def __init__(self, id: _Optional[str] = ..., rule_id: _Optional[str] = ..., rule_name: _Optional[str] = ..., evaluated_at: _Optional[int] = ..., duration_ms: _Optional[int] = ..., condition_matched: bool = ..., matched_count: _Optional[int] = ..., recipients_resolved: _Optional[int] = ..., recipients_notified: _Optional[int] = ..., recipients_dropped: _Optional[int] = ..., notification_sent: bool = ..., group_value: _Optional[str] = ..., error: _Optional[str] = ..., batch_id: _Optional[str] = ..., is_test: bool = ..., status: _Optional[_Union[ExecutionStatus, str]] = ...) -> None: ...
