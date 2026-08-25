from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DirectPriority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRIORITY_UNSPECIFIED: _ClassVar[DirectPriority]
    PRIORITY_LOW: _ClassVar[DirectPriority]
    PRIORITY_MEDIUM: _ClassVar[DirectPriority]
    PRIORITY_HIGH: _ClassVar[DirectPriority]

class DirectTheme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THEME_UNSPECIFIED: _ClassVar[DirectTheme]
    THEME_INFO: _ClassVar[DirectTheme]
    THEME_SUCCESS: _ClassVar[DirectTheme]
    THEME_WARNING: _ClassVar[DirectTheme]
    THEME_ERROR: _ClassVar[DirectTheme]
PRIORITY_UNSPECIFIED: DirectPriority
PRIORITY_LOW: DirectPriority
PRIORITY_MEDIUM: DirectPriority
PRIORITY_HIGH: DirectPriority
THEME_UNSPECIFIED: DirectTheme
THEME_INFO: DirectTheme
THEME_SUCCESS: DirectTheme
THEME_WARNING: DirectTheme
THEME_ERROR: DirectTheme

class DirectAction(_message.Message):
    __slots__ = ("text", "url")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    text: str
    url: str
    def __init__(self, text: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class DirectEmailRequest(_message.Message):
    __slots__ = ("to", "subject", "body", "is_html", "template_id", "connection_id", "priority", "theme", "facts", "actions")
    class FactsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TO_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    IS_HTML_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    FACTS_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    to: str
    subject: str
    body: str
    is_html: bool
    template_id: str
    connection_id: str
    priority: DirectPriority
    theme: DirectTheme
    facts: _containers.ScalarMap[str, str]
    actions: _containers.RepeatedCompositeFieldContainer[DirectAction]
    def __init__(self, to: _Optional[str] = ..., subject: _Optional[str] = ..., body: _Optional[str] = ..., is_html: bool = ..., template_id: _Optional[str] = ..., connection_id: _Optional[str] = ..., priority: _Optional[_Union[DirectPriority, str]] = ..., theme: _Optional[_Union[DirectTheme, str]] = ..., facts: _Optional[_Mapping[str, str]] = ..., actions: _Optional[_Iterable[_Union[DirectAction, _Mapping]]] = ...) -> None: ...

class DirectWhatsAppTemplateRequest(_message.Message):
    __slots__ = ("phone_number", "template_name", "language_code", "connection_id", "priority", "theme")
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    phone_number: str
    template_name: str
    language_code: str
    connection_id: str
    priority: DirectPriority
    theme: DirectTheme
    def __init__(self, phone_number: _Optional[str] = ..., template_name: _Optional[str] = ..., language_code: _Optional[str] = ..., connection_id: _Optional[str] = ..., priority: _Optional[_Union[DirectPriority, str]] = ..., theme: _Optional[_Union[DirectTheme, str]] = ...) -> None: ...

class DirectWhatsAppMessageRequest(_message.Message):
    __slots__ = ("phone_number", "body", "connection_id", "priority", "theme")
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    phone_number: str
    body: str
    connection_id: str
    priority: DirectPriority
    theme: DirectTheme
    def __init__(self, phone_number: _Optional[str] = ..., body: _Optional[str] = ..., connection_id: _Optional[str] = ..., priority: _Optional[_Union[DirectPriority, str]] = ..., theme: _Optional[_Union[DirectTheme, str]] = ...) -> None: ...

class DirectTeamsRequest(_message.Message):
    __slots__ = ("subject", "body", "webhook_url", "connection_id", "priority", "theme", "facts", "actions")
    class FactsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_URL_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    FACTS_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    subject: str
    body: str
    webhook_url: str
    connection_id: str
    priority: DirectPriority
    theme: DirectTheme
    facts: _containers.ScalarMap[str, str]
    actions: _containers.RepeatedCompositeFieldContainer[DirectAction]
    def __init__(self, subject: _Optional[str] = ..., body: _Optional[str] = ..., webhook_url: _Optional[str] = ..., connection_id: _Optional[str] = ..., priority: _Optional[_Union[DirectPriority, str]] = ..., theme: _Optional[_Union[DirectTheme, str]] = ..., facts: _Optional[_Mapping[str, str]] = ..., actions: _Optional[_Iterable[_Union[DirectAction, _Mapping]]] = ...) -> None: ...

class DirectSlackDMRequest(_message.Message):
    __slots__ = ("user_id", "user_email", "subject", "body", "connection_id", "priority", "theme", "facts", "actions", "attachments", "image_url", "image_alt_text")
    class FactsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    FACTS_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_ALT_TEXT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    user_email: str
    subject: str
    body: str
    connection_id: str
    priority: DirectPriority
    theme: DirectTheme
    facts: _containers.ScalarMap[str, str]
    actions: _containers.RepeatedCompositeFieldContainer[DirectAction]
    attachments: _containers.RepeatedCompositeFieldContainer[DirectAttachment]
    image_url: str
    image_alt_text: str
    def __init__(self, user_id: _Optional[str] = ..., user_email: _Optional[str] = ..., subject: _Optional[str] = ..., body: _Optional[str] = ..., connection_id: _Optional[str] = ..., priority: _Optional[_Union[DirectPriority, str]] = ..., theme: _Optional[_Union[DirectTheme, str]] = ..., facts: _Optional[_Mapping[str, str]] = ..., actions: _Optional[_Iterable[_Union[DirectAction, _Mapping]]] = ..., attachments: _Optional[_Iterable[_Union[DirectAttachment, _Mapping]]] = ..., image_url: _Optional[str] = ..., image_alt_text: _Optional[str] = ...) -> None: ...

class DirectAttachment(_message.Message):
    __slots__ = ("filename", "content_type", "content")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    filename: str
    content_type: str
    content: bytes
    def __init__(self, filename: _Optional[str] = ..., content_type: _Optional[str] = ..., content: _Optional[bytes] = ...) -> None: ...

class DirectSlackRequest(_message.Message):
    __slots__ = ("subject", "body", "webhook_url", "connection_id", "channel_id", "priority", "theme", "facts", "actions", "attachments", "image_url", "image_alt_text")
    class FactsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_URL_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    FACTS_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_ALT_TEXT_FIELD_NUMBER: _ClassVar[int]
    subject: str
    body: str
    webhook_url: str
    connection_id: str
    channel_id: str
    priority: DirectPriority
    theme: DirectTheme
    facts: _containers.ScalarMap[str, str]
    actions: _containers.RepeatedCompositeFieldContainer[DirectAction]
    attachments: _containers.RepeatedCompositeFieldContainer[DirectAttachment]
    image_url: str
    image_alt_text: str
    def __init__(self, subject: _Optional[str] = ..., body: _Optional[str] = ..., webhook_url: _Optional[str] = ..., connection_id: _Optional[str] = ..., channel_id: _Optional[str] = ..., priority: _Optional[_Union[DirectPriority, str]] = ..., theme: _Optional[_Union[DirectTheme, str]] = ..., facts: _Optional[_Mapping[str, str]] = ..., actions: _Optional[_Iterable[_Union[DirectAction, _Mapping]]] = ..., attachments: _Optional[_Iterable[_Union[DirectAttachment, _Mapping]]] = ..., image_url: _Optional[str] = ..., image_alt_text: _Optional[str] = ...) -> None: ...

class DirectPushRequest(_message.Message):
    __slots__ = ("user_id", "subject", "body", "connection_id", "priority", "theme", "link_url", "actions")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    LINK_URL_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    subject: str
    body: str
    connection_id: str
    priority: DirectPriority
    theme: DirectTheme
    link_url: str
    actions: _containers.RepeatedCompositeFieldContainer[DirectAction]
    def __init__(self, user_id: _Optional[str] = ..., subject: _Optional[str] = ..., body: _Optional[str] = ..., connection_id: _Optional[str] = ..., priority: _Optional[_Union[DirectPriority, str]] = ..., theme: _Optional[_Union[DirectTheme, str]] = ..., link_url: _Optional[str] = ..., actions: _Optional[_Iterable[_Union[DirectAction, _Mapping]]] = ...) -> None: ...

class GetMessageStatusRequest(_message.Message):
    __slots__ = ("message_id",)
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    def __init__(self, message_id: _Optional[str] = ...) -> None: ...

class DirectSendResponse(_message.Message):
    __slots__ = ("message_id",)
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    def __init__(self, message_id: _Optional[str] = ...) -> None: ...

class ChannelStatusEntry(_message.Message):
    __slots__ = ("channel", "status", "sent_at", "delivered_at", "read_at")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SENT_AT_FIELD_NUMBER: _ClassVar[int]
    DELIVERED_AT_FIELD_NUMBER: _ClassVar[int]
    READ_AT_FIELD_NUMBER: _ClassVar[int]
    channel: str
    status: str
    sent_at: str
    delivered_at: str
    read_at: str
    def __init__(self, channel: _Optional[str] = ..., status: _Optional[str] = ..., sent_at: _Optional[str] = ..., delivered_at: _Optional[str] = ..., read_at: _Optional[str] = ...) -> None: ...

class MessageStatusResponse(_message.Message):
    __slots__ = ("message_id", "recipient", "created_at", "channels")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    recipient: str
    created_at: str
    channels: _containers.RepeatedCompositeFieldContainer[ChannelStatusEntry]
    def __init__(self, message_id: _Optional[str] = ..., recipient: _Optional[str] = ..., created_at: _Optional[str] = ..., channels: _Optional[_Iterable[_Union[ChannelStatusEntry, _Mapping]]] = ...) -> None: ...
