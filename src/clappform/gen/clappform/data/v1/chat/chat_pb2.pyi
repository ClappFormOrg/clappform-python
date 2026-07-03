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
    ROOM_NOT_FOUND: _ClassVar[ErrorCode]
    MESSAGE_INVALID: _ClassVar[ErrorCode]
    INTERNAL_ERROR: _ClassVar[ErrorCode]
    RATE_LIMITED: _ClassVar[ErrorCode]
    UNAUTHORIZED: _ClassVar[ErrorCode]
    CONFLICT: _ClassVar[ErrorCode]

class RoomAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROOM_ACTION_UNKNOWN: _ClassVar[RoomAction]
    ROOM_ACTION_CREATED: _ClassVar[RoomAction]
    ROOM_ACTION_UPDATED: _ClassVar[RoomAction]
    ROOM_ACTION_DELETED: _ClassVar[RoomAction]
UNKNOWN: ErrorCode
INVALID_ARGUMENT: ErrorCode
PERMISSION_DENIED: ErrorCode
ROOM_NOT_FOUND: ErrorCode
MESSAGE_INVALID: ErrorCode
INTERNAL_ERROR: ErrorCode
RATE_LIMITED: ErrorCode
UNAUTHORIZED: ErrorCode
CONFLICT: ErrorCode
ROOM_ACTION_UNKNOWN: RoomAction
ROOM_ACTION_CREATED: RoomAction
ROOM_ACTION_UPDATED: RoomAction
ROOM_ACTION_DELETED: RoomAction

class FileUploadRequest(_message.Message):
    __slots__ = ("filenames", "collection")
    FILENAMES_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    filenames: _containers.RepeatedScalarFieldContainer[str]
    collection: str
    def __init__(self, filenames: _Optional[_Iterable[str]] = ..., collection: _Optional[str] = ...) -> None: ...

class FileUploadResponse(_message.Message):
    __slots__ = ("urls",)
    URLS_FIELD_NUMBER: _ClassVar[int]
    urls: _containers.RepeatedCompositeFieldContainer[FileUploadUrl]
    def __init__(self, urls: _Optional[_Iterable[_Union[FileUploadUrl, _Mapping]]] = ...) -> None: ...

class FileUploadUrl(_message.Message):
    __slots__ = ("filename", "url")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    filename: str
    url: str
    def __init__(self, filename: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class FileDeleteRequest(_message.Message):
    __slots__ = ("document_id", "collection", "filename")
    DOCUMENT_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    document_id: str
    collection: str
    filename: str
    def __init__(self, document_id: _Optional[str] = ..., collection: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("code", "message", "details")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    message: str
    details: str
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., message: _Optional[str] = ..., details: _Optional[str] = ...) -> None: ...

class StreamMessageResponse(_message.Message):
    __slots__ = ("app_id", "message", "room", "error")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    message: Message
    room: Room
    error: Error
    def __init__(self, app_id: _Optional[str] = ..., message: _Optional[_Union[Message, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class StreamMessageRequest(_message.Message):
    __slots__ = ("id", "payload")
    ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    id: str
    payload: StreamMessageRequestPayload
    def __init__(self, id: _Optional[str] = ..., payload: _Optional[_Union[StreamMessageRequestPayload, _Mapping]] = ...) -> None: ...

class StreamMessageRequestPayload(_message.Message):
    __slots__ = ("app_id", "message", "room")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    message: Message
    room: Room
    def __init__(self, app_id: _Optional[str] = ..., message: _Optional[_Union[Message, _Mapping]] = ..., room: _Optional[_Union[Room, _Mapping]] = ...) -> None: ...

class Content(_message.Message):
    __slots__ = ("type", "text")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    type: str
    text: str
    def __init__(self, type: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

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
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

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

class Room(_message.Message):
    __slots__ = ("id", "name", "created_at", "action", "settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    created_at: int
    action: RoomAction
    settings: RoomSettings
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., created_at: _Optional[int] = ..., action: _Optional[_Union[RoomAction, str]] = ..., settings: _Optional[_Union[RoomSettings, _Mapping]] = ...) -> None: ...

class RoomSettings(_message.Message):
    __slots__ = ("inherit", "locale", "name", "occupation", "traits")
    INHERIT_FIELD_NUMBER: _ClassVar[int]
    LOCALE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OCCUPATION_FIELD_NUMBER: _ClassVar[int]
    TRAITS_FIELD_NUMBER: _ClassVar[int]
    inherit: bool
    locale: str
    name: str
    occupation: str
    traits: str
    def __init__(self, inherit: bool = ..., locale: _Optional[str] = ..., name: _Optional[str] = ..., occupation: _Optional[str] = ..., traits: _Optional[str] = ...) -> None: ...

class Rooms(_message.Message):
    __slots__ = ("rooms",)
    ROOMS_FIELD_NUMBER: _ClassVar[int]
    rooms: _containers.RepeatedCompositeFieldContainer[Room]
    def __init__(self, rooms: _Optional[_Iterable[_Union[Room, _Mapping]]] = ...) -> None: ...

class GetRoomsRequest(_message.Message):
    __slots__ = ("app_id",)
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    def __init__(self, app_id: _Optional[str] = ...) -> None: ...

class UpdateRoomRequest(_message.Message):
    __slots__ = ("id", "room")
    ID_FIELD_NUMBER: _ClassVar[int]
    ROOM_FIELD_NUMBER: _ClassVar[int]
    id: str
    room: RoomUpdate
    def __init__(self, id: _Optional[str] = ..., room: _Optional[_Union[RoomUpdate, _Mapping]] = ...) -> None: ...

class RoomUpdate(_message.Message):
    __slots__ = ("app_id", "name", "settings")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    name: str
    settings: RoomSettings
    def __init__(self, app_id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[_Union[RoomSettings, _Mapping]] = ...) -> None: ...

class DeleteRoomRequest(_message.Message):
    __slots__ = ("app_id", "id")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    id: str
    def __init__(self, app_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class GetMessagesRequest(_message.Message):
    __slots__ = ("app_id", "id", "cursor")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    id: str
    cursor: int
    def __init__(self, app_id: _Optional[str] = ..., id: _Optional[str] = ..., cursor: _Optional[int] = ...) -> None: ...
