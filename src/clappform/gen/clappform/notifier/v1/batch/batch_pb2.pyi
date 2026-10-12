from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class channel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_CHANNEL: _ClassVar[channel]
    EMAIL: _ClassVar[channel]
    TEAMS: _ClassVar[channel]
    PUSH: _ClassVar[channel]
    WHATSAPP: _ClassVar[channel]
    SLACK: _ClassVar[channel]
    AUTO: _ClassVar[channel]

class condition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_CONDITION: _ClassVar[condition]
    NOT_READ: _ClassVar[condition]
    NOT_ACKNOWLEDGED: _ClassVar[condition]
    IS_READ: _ClassVar[condition]
    IS_ACKNOWLEDGED: _ClassVar[condition]
    CUSTOM_WEBHOOK: _ClassVar[condition]

class action_type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_ACTION_TYPE: _ClassVar[action_type]
    BUTTON: _ClassVar[action_type]

class priority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_PRIORITY: _ClassVar[priority]
    LOW: _ClassVar[priority]
    MEDIUM: _ClassVar[priority]
    HIGH: _ClassVar[priority]

class theme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_THEME: _ClassVar[theme]
    INFO: _ClassVar[theme]
    SUCCESS: _ClassVar[theme]
    WARNING: _ClassVar[theme]
    ERROR: _ClassVar[theme]
UNSPECIFIED_CHANNEL: channel
EMAIL: channel
TEAMS: channel
PUSH: channel
WHATSAPP: channel
SLACK: channel
AUTO: channel
UNSPECIFIED_CONDITION: condition
NOT_READ: condition
NOT_ACKNOWLEDGED: condition
IS_READ: condition
IS_ACKNOWLEDGED: condition
CUSTOM_WEBHOOK: condition
UNSPECIFIED_ACTION_TYPE: action_type
BUTTON: action_type
UNSPECIFIED_PRIORITY: priority
LOW: priority
MEDIUM: priority
HIGH: priority
UNSPECIFIED_THEME: theme
INFO: theme
SUCCESS: theme
WARNING: theme
ERROR: theme

class Recipient(_message.Message):
    __slots__ = ("user_id", "user_first_name", "user_last_name", "user_email", "user_phone", "variables")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_PHONE_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    user_first_name: str
    user_last_name: str
    user_email: str
    user_phone: str
    variables: bytes
    def __init__(self, user_id: _Optional[str] = ..., user_first_name: _Optional[str] = ..., user_last_name: _Optional[str] = ..., user_email: _Optional[str] = ..., user_phone: _Optional[str] = ..., variables: _Optional[bytes] = ...) -> None: ...

class Action(_message.Message):
    __slots__ = ("id", "type", "text", "url", "data")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: action_type
    text: str
    url: str
    data: bytes
    def __init__(self, id: _Optional[str] = ..., type: _Optional[_Union[action_type, str]] = ..., text: _Optional[str] = ..., url: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class Attachment(_message.Message):
    __slots__ = ("filename", "content_type", "content", "disposition", "content_id")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    DISPOSITION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_ID_FIELD_NUMBER: _ClassVar[int]
    filename: str
    content_type: str
    content: bytes
    disposition: str
    content_id: str
    def __init__(self, filename: _Optional[str] = ..., content_type: _Optional[str] = ..., content: _Optional[bytes] = ..., disposition: _Optional[str] = ..., content_id: _Optional[str] = ...) -> None: ...

class EmailContent(_message.Message):
    __slots__ = ("subject", "body", "facts", "is_html", "attachments", "template_id", "from_email", "from_name", "category", "reply_to")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    FACTS_FIELD_NUMBER: _ClassVar[int]
    IS_HTML_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_EMAIL_FIELD_NUMBER: _ClassVar[int]
    FROM_NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_FIELD_NUMBER: _ClassVar[int]
    subject: str
    body: str
    facts: bytes
    is_html: bool
    attachments: _containers.RepeatedCompositeFieldContainer[Attachment]
    template_id: str
    from_email: str
    from_name: str
    category: _containers.RepeatedScalarFieldContainer[str]
    reply_to: str
    def __init__(self, subject: _Optional[str] = ..., body: _Optional[str] = ..., facts: _Optional[bytes] = ..., is_html: bool = ..., attachments: _Optional[_Iterable[_Union[Attachment, _Mapping]]] = ..., template_id: _Optional[str] = ..., from_email: _Optional[str] = ..., from_name: _Optional[str] = ..., category: _Optional[_Iterable[str]] = ..., reply_to: _Optional[str] = ...) -> None: ...

class TeamsContent(_message.Message):
    __slots__ = ("subject", "body", "facts", "attachments", "webhook_url")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    FACTS_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_URL_FIELD_NUMBER: _ClassVar[int]
    subject: str
    body: str
    facts: bytes
    attachments: _containers.RepeatedCompositeFieldContainer[Attachment]
    webhook_url: str
    def __init__(self, subject: _Optional[str] = ..., body: _Optional[str] = ..., facts: _Optional[bytes] = ..., attachments: _Optional[_Iterable[_Union[Attachment, _Mapping]]] = ..., webhook_url: _Optional[str] = ...) -> None: ...

class WhatsAppContent(_message.Message):
    __slots__ = ("body", "media_url", "media_file", "template_name", "language_code")
    BODY_FIELD_NUMBER: _ClassVar[int]
    MEDIA_URL_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FILE_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    body: str
    media_url: str
    media_file: Attachment
    template_name: str
    language_code: str
    def __init__(self, body: _Optional[str] = ..., media_url: _Optional[str] = ..., media_file: _Optional[_Union[Attachment, _Mapping]] = ..., template_name: _Optional[str] = ..., language_code: _Optional[str] = ...) -> None: ...

class PushContent(_message.Message):
    __slots__ = ("subject", "body", "link_url", "attachments")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    LINK_URL_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    subject: str
    body: str
    link_url: str
    attachments: _containers.RepeatedCompositeFieldContainer[Attachment]
    def __init__(self, subject: _Optional[str] = ..., body: _Optional[str] = ..., link_url: _Optional[str] = ..., attachments: _Optional[_Iterable[_Union[Attachment, _Mapping]]] = ...) -> None: ...

class SlackContent(_message.Message):
    __slots__ = ("subject", "body", "facts", "webhook_url", "attachments", "image_url", "image_alt_text")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    FACTS_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_URL_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_ALT_TEXT_FIELD_NUMBER: _ClassVar[int]
    subject: str
    body: str
    facts: bytes
    webhook_url: str
    attachments: _containers.RepeatedCompositeFieldContainer[Attachment]
    image_url: str
    image_alt_text: str
    def __init__(self, subject: _Optional[str] = ..., body: _Optional[str] = ..., facts: _Optional[bytes] = ..., webhook_url: _Optional[str] = ..., attachments: _Optional[_Iterable[_Union[Attachment, _Mapping]]] = ..., image_url: _Optional[str] = ..., image_alt_text: _Optional[str] = ...) -> None: ...

class stepCondition(_message.Message):
    __slots__ = ("type", "previous_step_id", "condition_quorum")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_STEP_ID_FIELD_NUMBER: _ClassVar[int]
    CONDITION_QUORUM_FIELD_NUMBER: _ClassVar[int]
    type: condition
    previous_step_id: str
    condition_quorum: str
    def __init__(self, type: _Optional[_Union[condition, str]] = ..., previous_step_id: _Optional[str] = ..., condition_quorum: _Optional[str] = ...) -> None: ...

class NotificationStep(_message.Message):
    __slots__ = ("step_id", "step_order", "channel", "recipients", "email", "teams", "whatsapp", "push", "slack", "step_variables", "delay_seconds", "conditions", "require_delay_and_condition", "actions")
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    STEP_ORDER_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    WHATSAPP_FIELD_NUMBER: _ClassVar[int]
    PUSH_FIELD_NUMBER: _ClassVar[int]
    SLACK_FIELD_NUMBER: _ClassVar[int]
    STEP_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    DELAY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_DELAY_AND_CONDITION_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    step_id: str
    step_order: int
    channel: channel
    recipients: _containers.RepeatedCompositeFieldContainer[Recipient]
    email: EmailContent
    teams: TeamsContent
    whatsapp: WhatsAppContent
    push: PushContent
    slack: SlackContent
    step_variables: bytes
    delay_seconds: int
    conditions: _containers.RepeatedCompositeFieldContainer[stepCondition]
    require_delay_and_condition: bool
    actions: _containers.RepeatedCompositeFieldContainer[Action]
    def __init__(self, step_id: _Optional[str] = ..., step_order: _Optional[int] = ..., channel: _Optional[_Union[channel, str]] = ..., recipients: _Optional[_Iterable[_Union[Recipient, _Mapping]]] = ..., email: _Optional[_Union[EmailContent, _Mapping]] = ..., teams: _Optional[_Union[TeamsContent, _Mapping]] = ..., whatsapp: _Optional[_Union[WhatsAppContent, _Mapping]] = ..., push: _Optional[_Union[PushContent, _Mapping]] = ..., slack: _Optional[_Union[SlackContent, _Mapping]] = ..., step_variables: _Optional[bytes] = ..., delay_seconds: _Optional[int] = ..., conditions: _Optional[_Iterable[_Union[stepCondition, _Mapping]]] = ..., require_delay_and_condition: bool = ..., actions: _Optional[_Iterable[_Union[Action, _Mapping]]] = ...) -> None: ...

class StopConditions(_message.Message):
    __slots__ = ("stop_on_read", "stop_on_action", "stop_on_reply", "max_attempts")
    STOP_ON_READ_FIELD_NUMBER: _ClassVar[int]
    STOP_ON_ACTION_FIELD_NUMBER: _ClassVar[int]
    STOP_ON_REPLY_FIELD_NUMBER: _ClassVar[int]
    MAX_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    stop_on_read: bool
    stop_on_action: bool
    stop_on_reply: bool
    max_attempts: int
    def __init__(self, stop_on_read: bool = ..., stop_on_action: bool = ..., stop_on_reply: bool = ..., max_attempts: _Optional[int] = ...) -> None: ...

class BatchRequest(_message.Message):
    __slots__ = ("steps", "default_variables", "default_actions", "stop_conditions", "priority", "theme", "start_delivery_at")
    STEPS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    STOP_CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    START_DELIVERY_AT_FIELD_NUMBER: _ClassVar[int]
    steps: _containers.RepeatedCompositeFieldContainer[NotificationStep]
    default_variables: bytes
    default_actions: _containers.RepeatedCompositeFieldContainer[Action]
    stop_conditions: StopConditions
    priority: priority
    theme: theme
    start_delivery_at: int
    def __init__(self, steps: _Optional[_Iterable[_Union[NotificationStep, _Mapping]]] = ..., default_variables: _Optional[bytes] = ..., default_actions: _Optional[_Iterable[_Union[Action, _Mapping]]] = ..., stop_conditions: _Optional[_Union[StopConditions, _Mapping]] = ..., priority: _Optional[_Union[priority, str]] = ..., theme: _Optional[_Union[theme, str]] = ..., start_delivery_at: _Optional[int] = ...) -> None: ...

class GetStatus(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[_Iterable[str]] = ...) -> None: ...

class BatchProgress(_message.Message):
    __slots__ = ("total_recipients", "queued", "accepted", "rejected", "total_steps")
    TOTAL_RECIPIENTS_FIELD_NUMBER: _ClassVar[int]
    QUEUED_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    REJECTED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_STEPS_FIELD_NUMBER: _ClassVar[int]
    total_recipients: int
    queued: int
    accepted: int
    rejected: int
    total_steps: int
    def __init__(self, total_recipients: _Optional[int] = ..., queued: _Optional[int] = ..., accepted: _Optional[int] = ..., rejected: _Optional[int] = ..., total_steps: _Optional[int] = ...) -> None: ...

class BatchStatus(_message.Message):
    __slots__ = ("batch_id", "status", "status_url", "failed_step_ids")
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_URL_FIELD_NUMBER: _ClassVar[int]
    FAILED_STEP_IDS_FIELD_NUMBER: _ClassVar[int]
    batch_id: str
    status: BatchProgress
    status_url: str
    failed_step_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, batch_id: _Optional[str] = ..., status: _Optional[_Union[BatchProgress, _Mapping]] = ..., status_url: _Optional[str] = ..., failed_step_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class EmailEvent(_message.Message):
    __slots__ = ("email", "timestamp", "event", "sg_event_id", "sg_message_id", "custom_args", "reason", "url", "category")
    class CustomArgsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    SG_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SG_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_ARGS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    email: str
    timestamp: int
    event: str
    sg_event_id: str
    sg_message_id: str
    custom_args: _containers.ScalarMap[str, str]
    reason: str
    url: str
    category: str
    def __init__(self, email: _Optional[str] = ..., timestamp: _Optional[int] = ..., event: _Optional[str] = ..., sg_event_id: _Optional[str] = ..., sg_message_id: _Optional[str] = ..., custom_args: _Optional[_Mapping[str, str]] = ..., reason: _Optional[str] = ..., url: _Optional[str] = ..., category: _Optional[str] = ...) -> None: ...
