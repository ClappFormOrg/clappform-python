from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HealthStatus(_message.Message):
    __slots__ = ("service", "timestamp")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    service: str
    timestamp: str
    def __init__(self, service: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class MessageRequest(_message.Message):
    __slots__ = ("phone_number", "message")
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    phone_number: str
    message: str
    def __init__(self, phone_number: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class MessageResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: int
    message: str
    def __init__(self, status: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class TemplateRequest(_message.Message):
    __slots__ = ("phone_number", "template_name", "language_code")
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    phone_number: str
    template_name: str
    language_code: str
    def __init__(self, phone_number: _Optional[str] = ..., template_name: _Optional[str] = ..., language_code: _Optional[str] = ...) -> None: ...

class WebhookVerifyResponse(_message.Message):
    __slots__ = ("challenge",)
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    challenge: str
    def __init__(self, challenge: _Optional[str] = ...) -> None: ...

class WebhookEventRequest(_message.Message):
    __slots__ = ("object", "entry")
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    object: str
    entry: _containers.RepeatedCompositeFieldContainer[WebhookEntry]
    def __init__(self, object: _Optional[str] = ..., entry: _Optional[_Iterable[_Union[WebhookEntry, _Mapping]]] = ...) -> None: ...

class WebhookEntry(_message.Message):
    __slots__ = ("id", "changes")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    id: str
    changes: _containers.RepeatedCompositeFieldContainer[WebhookChange]
    def __init__(self, id: _Optional[str] = ..., changes: _Optional[_Iterable[_Union[WebhookChange, _Mapping]]] = ...) -> None: ...

class WebhookChange(_message.Message):
    __slots__ = ("field", "value")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    field: str
    value: WebhookValue
    def __init__(self, field: _Optional[str] = ..., value: _Optional[_Union[WebhookValue, _Mapping]] = ...) -> None: ...

class WebhookValue(_message.Message):
    __slots__ = ("messaging_product", "metadata", "contacts", "messages", "statuses")
    MESSAGING_PRODUCT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CONTACTS_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    messaging_product: str
    metadata: WebhookMetadata
    contacts: _containers.RepeatedCompositeFieldContainer[WebhookContact]
    messages: _containers.RepeatedCompositeFieldContainer[WebhookMessage]
    statuses: _containers.RepeatedCompositeFieldContainer[WebhookStatus]
    def __init__(self, messaging_product: _Optional[str] = ..., metadata: _Optional[_Union[WebhookMetadata, _Mapping]] = ..., contacts: _Optional[_Iterable[_Union[WebhookContact, _Mapping]]] = ..., messages: _Optional[_Iterable[_Union[WebhookMessage, _Mapping]]] = ..., statuses: _Optional[_Iterable[_Union[WebhookStatus, _Mapping]]] = ...) -> None: ...

class WebhookMetadata(_message.Message):
    __slots__ = ("display_phone_number", "phone_number_id")
    DISPLAY_PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_ID_FIELD_NUMBER: _ClassVar[int]
    display_phone_number: str
    phone_number_id: str
    def __init__(self, display_phone_number: _Optional[str] = ..., phone_number_id: _Optional[str] = ...) -> None: ...

class WebhookContact(_message.Message):
    __slots__ = ("profile", "wa_id")
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    WA_ID_FIELD_NUMBER: _ClassVar[int]
    profile: str
    wa_id: str
    def __init__(self, profile: _Optional[str] = ..., wa_id: _Optional[str] = ...) -> None: ...

class WebhookMessage(_message.Message):
    __slots__ = ("id", "timestamp", "type", "text", "interactive", "button", "image", "document", "context")
    ID_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    INTERACTIVE_FIELD_NUMBER: _ClassVar[int]
    BUTTON_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    id: str
    timestamp: int
    type: str
    text: WebhookTextMessage
    interactive: WebhookInteractiveMessage
    button: WebhookButtonMessage
    image: WebhookImageMessage
    document: WebhookDocumentMessage
    context: WebhookContext
    def __init__(self, id: _Optional[str] = ..., timestamp: _Optional[int] = ..., type: _Optional[str] = ..., text: _Optional[_Union[WebhookTextMessage, _Mapping]] = ..., interactive: _Optional[_Union[WebhookInteractiveMessage, _Mapping]] = ..., button: _Optional[_Union[WebhookButtonMessage, _Mapping]] = ..., image: _Optional[_Union[WebhookImageMessage, _Mapping]] = ..., document: _Optional[_Union[WebhookDocumentMessage, _Mapping]] = ..., context: _Optional[_Union[WebhookContext, _Mapping]] = ..., **kwargs) -> None: ...

class WebhookTextMessage(_message.Message):
    __slots__ = ("body",)
    BODY_FIELD_NUMBER: _ClassVar[int]
    body: str
    def __init__(self, body: _Optional[str] = ...) -> None: ...

class WebhookInteractiveMessage(_message.Message):
    __slots__ = ("type", "button_reply", "list_reply", "nfm_reply")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BUTTON_REPLY_FIELD_NUMBER: _ClassVar[int]
    LIST_REPLY_FIELD_NUMBER: _ClassVar[int]
    NFM_REPLY_FIELD_NUMBER: _ClassVar[int]
    type: str
    button_reply: WebhookButtonReply
    list_reply: WebhookListReply
    nfm_reply: WebhookFlowReply
    def __init__(self, type: _Optional[str] = ..., button_reply: _Optional[_Union[WebhookButtonReply, _Mapping]] = ..., list_reply: _Optional[_Union[WebhookListReply, _Mapping]] = ..., nfm_reply: _Optional[_Union[WebhookFlowReply, _Mapping]] = ...) -> None: ...

class WebhookButtonReply(_message.Message):
    __slots__ = ("id", "title")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ...) -> None: ...

class WebhookListReply(_message.Message):
    __slots__ = ("id", "title", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class WebhookFlowReply(_message.Message):
    __slots__ = ("name", "body", "response_json")
    NAME_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_JSON_FIELD_NUMBER: _ClassVar[int]
    name: str
    body: str
    response_json: WebhookFlowResponse
    def __init__(self, name: _Optional[str] = ..., body: _Optional[str] = ..., response_json: _Optional[_Union[WebhookFlowResponse, _Mapping]] = ...) -> None: ...

class WebhookFlowResponse(_message.Message):
    __slots__ = ("flow_token", "form_data")
    class FormDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FLOW_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FORM_DATA_FIELD_NUMBER: _ClassVar[int]
    flow_token: str
    form_data: _containers.ScalarMap[str, str]
    def __init__(self, flow_token: _Optional[str] = ..., form_data: _Optional[_Mapping[str, str]] = ...) -> None: ...

class WebhookButtonMessage(_message.Message):
    __slots__ = ("text", "payload")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    text: str
    payload: str
    def __init__(self, text: _Optional[str] = ..., payload: _Optional[str] = ...) -> None: ...

class WebhookImageMessage(_message.Message):
    __slots__ = ("id", "mime_type", "caption")
    ID_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    CAPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    mime_type: str
    caption: str
    def __init__(self, id: _Optional[str] = ..., mime_type: _Optional[str] = ..., caption: _Optional[str] = ...) -> None: ...

class WebhookDocumentMessage(_message.Message):
    __slots__ = ("id", "mime_type", "filename", "caption")
    ID_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    CAPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    mime_type: str
    filename: str
    caption: str
    def __init__(self, id: _Optional[str] = ..., mime_type: _Optional[str] = ..., filename: _Optional[str] = ..., caption: _Optional[str] = ...) -> None: ...

class WebhookContext(_message.Message):
    __slots__ = ("id", "forwarded")
    FROM_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    FORWARDED_FIELD_NUMBER: _ClassVar[int]
    id: str
    forwarded: bool
    def __init__(self, id: _Optional[str] = ..., forwarded: bool = ..., **kwargs) -> None: ...

class WebhookStatus(_message.Message):
    __slots__ = ("id", "status", "timestamp", "recipient_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: str
    timestamp: int
    recipient_id: str
    def __init__(self, id: _Optional[str] = ..., status: _Optional[str] = ..., timestamp: _Optional[int] = ..., recipient_id: _Optional[str] = ...) -> None: ...

class WebhookEventResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
