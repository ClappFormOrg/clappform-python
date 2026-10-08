from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NotificationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_UNSPECIFIED: _ClassVar[NotificationStatus]
    SENT: _ClassVar[NotificationStatus]
    DELIVERED: _ClassVar[NotificationStatus]
    READ: _ClassVar[NotificationStatus]
    ACKNOWLEDGED: _ClassVar[NotificationStatus]
    FAILED: _ClassVar[NotificationStatus]
    SUPPRESSED: _ClassVar[NotificationStatus]
    DEFERRED: _ClassVar[NotificationStatus]

class NotificationPriority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRIORITY_UNSPECIFIED: _ClassVar[NotificationPriority]
    LOW: _ClassVar[NotificationPriority]
    NORMAL: _ClassVar[NotificationPriority]
    HIGH: _ClassVar[NotificationPriority]
    URGENT: _ClassVar[NotificationPriority]
STATUS_UNSPECIFIED: NotificationStatus
SENT: NotificationStatus
DELIVERED: NotificationStatus
READ: NotificationStatus
ACKNOWLEDGED: NotificationStatus
FAILED: NotificationStatus
SUPPRESSED: NotificationStatus
DEFERRED: NotificationStatus
PRIORITY_UNSPECIFIED: NotificationPriority
LOW: NotificationPriority
NORMAL: NotificationPriority
HIGH: NotificationPriority
URGENT: NotificationPriority

class Action(_message.Message):
    __slots__ = ("id", "type", "text", "url", "data")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    text: str
    url: str
    data: bytes
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., text: _Optional[str] = ..., url: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class PushNotification(_message.Message):
    __slots__ = ("id", "user_id", "batch_id", "step_id", "subject", "body", "priority", "actions", "variables", "created_at", "read_at", "acknowledged_at", "status")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    READ_AT_FIELD_NUMBER: _ClassVar[int]
    ACKNOWLEDGED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    batch_id: str
    step_id: str
    subject: str
    body: str
    priority: NotificationPriority
    actions: _containers.RepeatedCompositeFieldContainer[Action]
    variables: _containers.ScalarMap[str, str]
    created_at: str
    read_at: str
    acknowledged_at: str
    status: NotificationStatus
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., batch_id: _Optional[str] = ..., step_id: _Optional[str] = ..., subject: _Optional[str] = ..., body: _Optional[str] = ..., priority: _Optional[_Union[NotificationPriority, str]] = ..., actions: _Optional[_Iterable[_Union[Action, _Mapping]]] = ..., variables: _Optional[_Mapping[str, str]] = ..., created_at: _Optional[str] = ..., read_at: _Optional[str] = ..., acknowledged_at: _Optional[str] = ..., status: _Optional[_Union[NotificationStatus, str]] = ...) -> None: ...

class GetNotificationsRequest(_message.Message):
    __slots__ = ("user_id", "offset", "limit", "status_filter")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FILTER_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    offset: int
    limit: int
    status_filter: _containers.RepeatedScalarFieldContainer[NotificationStatus]
    def __init__(self, user_id: _Optional[str] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., status_filter: _Optional[_Iterable[_Union[NotificationStatus, str]]] = ...) -> None: ...

class GetNotificationsResponse(_message.Message):
    __slots__ = ("notifications", "offset", "limit", "total_count")
    NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    notifications: _containers.RepeatedCompositeFieldContainer[PushNotification]
    offset: int
    limit: int
    total_count: int
    def __init__(self, notifications: _Optional[_Iterable[_Union[PushNotification, _Mapping]]] = ..., offset: _Optional[int] = ..., limit: _Optional[int] = ..., total_count: _Optional[int] = ...) -> None: ...

class GetUnreadCountRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetUnreadCountResponse(_message.Message):
    __slots__ = ("user_id", "unread_count")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    UNREAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    unread_count: int
    def __init__(self, user_id: _Optional[str] = ..., unread_count: _Optional[int] = ...) -> None: ...

class MarkAsReadRequest(_message.Message):
    __slots__ = ("notification_id", "batch_id", "step_id", "user_id")
    NOTIFICATION_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    notification_id: str
    batch_id: str
    step_id: str
    user_id: str
    def __init__(self, notification_id: _Optional[str] = ..., batch_id: _Optional[str] = ..., step_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class MarkAsAcknowledgedRequest(_message.Message):
    __slots__ = ("notification_id", "batch_id", "step_id", "user_id")
    NOTIFICATION_ID_FIELD_NUMBER: _ClassVar[int]
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    notification_id: str
    batch_id: str
    step_id: str
    user_id: str
    def __init__(self, notification_id: _Optional[str] = ..., batch_id: _Optional[str] = ..., step_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class BulkUpdateStatusItem(_message.Message):
    __slots__ = ("batch_id", "step_id")
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    batch_id: str
    step_id: str
    def __init__(self, batch_id: _Optional[str] = ..., step_id: _Optional[str] = ...) -> None: ...

class BulkUpdateStatusRequest(_message.Message):
    __slots__ = ("items", "status")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[BulkUpdateStatusItem]
    status: str
    def __init__(self, items: _Optional[_Iterable[_Union[BulkUpdateStatusItem, _Mapping]]] = ..., status: _Optional[str] = ...) -> None: ...

class BulkUpdateStatusResponse(_message.Message):
    __slots__ = ("updated_count",)
    UPDATED_COUNT_FIELD_NUMBER: _ClassVar[int]
    updated_count: int
    def __init__(self, updated_count: _Optional[int] = ...) -> None: ...

class ListSuppressionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSuppressionsResponse(_message.Message):
    __slots__ = ("suppressed_emails", "count")
    SUPPRESSED_EMAILS_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    suppressed_emails: _containers.RepeatedScalarFieldContainer[str]
    count: int
    def __init__(self, suppressed_emails: _Optional[_Iterable[str]] = ..., count: _Optional[int] = ...) -> None: ...

class RemoveSuppressionRequest(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...
