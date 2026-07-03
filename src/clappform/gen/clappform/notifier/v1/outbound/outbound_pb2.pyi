from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class level(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[level]
    INFO: _ClassVar[level]
    WARNING: _ClassVar[level]
    ERROR: _ClassVar[level]
    CRITICAL: _ClassVar[level]

class status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_STATUS: _ClassVar[status]
    PENDING: _ClassVar[status]
    SENT: _ClassVar[status]
    READ: _ClassVar[status]
    FAILED: _ClassVar[status]
    ARCHIVED: _ClassVar[status]

class type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSET: _ClassVar[type]
    WHATSAPP_MESSAGE: _ClassVar[type]
    WHATSAPP_TEMPLATE: _ClassVar[type]
    INBOX_NOTIFICATION: _ClassVar[type]
    TEAMS_MESSAGE: _ClassVar[type]
    SLACK_MESSAGE: _ClassVar[type]
    EMAIL: _ClassVar[type]
UNSPECIFIED: level
INFO: level
WARNING: level
ERROR: level
CRITICAL: level
NO_STATUS: status
PENDING: status
SENT: status
READ: status
FAILED: status
ARCHIVED: status
UNSET: type
WHATSAPP_MESSAGE: type
WHATSAPP_TEMPLATE: type
INBOX_NOTIFICATION: type
TEAMS_MESSAGE: type
SLACK_MESSAGE: type
EMAIL: type

class Message(_message.Message):
    __slots__ = ("id", "level", "type", "metadata", "status", "created_at", "delivered_at", "read_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELIVERED_AT_FIELD_NUMBER: _ClassVar[int]
    READ_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    level: level
    type: type
    metadata: bytes
    status: status
    created_at: str
    delivered_at: str
    read_at: str
    def __init__(self, id: _Optional[str] = ..., level: _Optional[_Union[level, str]] = ..., type: _Optional[_Union[type, str]] = ..., metadata: _Optional[bytes] = ..., status: _Optional[_Union[status, str]] = ..., created_at: _Optional[str] = ..., delivered_at: _Optional[str] = ..., read_at: _Optional[str] = ...) -> None: ...

class MessageResponse(_message.Message):
    __slots__ = ("message_ids",)
    MESSAGE_IDS_FIELD_NUMBER: _ClassVar[int]
    message_ids: _containers.RepeatedCompositeFieldContainer[_commons_pb2.Read]
    def __init__(self, message_ids: _Optional[_Iterable[_Union[_commons_pb2.Read, _Mapping]]] = ...) -> None: ...

class Messages(_message.Message):
    __slots__ = ("messages", "pagination")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[Message]
    pagination: _commons_pb2.Pagination
    def __init__(self, messages: _Optional[_Iterable[_Union[Message, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
