from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpsertConnectionRequest(_message.Message):
    __slots__ = ("channel", "provider", "config", "config_preview")
    class ConfigEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class ConfigPreviewEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    CONFIG_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    channel: str
    provider: str
    config: _containers.ScalarMap[str, str]
    config_preview: _containers.ScalarMap[str, str]
    def __init__(self, channel: _Optional[str] = ..., provider: _Optional[str] = ..., config: _Optional[_Mapping[str, str]] = ..., config_preview: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GetConnectionRequest(_message.Message):
    __slots__ = ("channel",)
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    channel: str
    def __init__(self, channel: _Optional[str] = ...) -> None: ...

class DeleteConnectionRequest(_message.Message):
    __slots__ = ("channel",)
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    channel: str
    def __init__(self, channel: _Optional[str] = ...) -> None: ...

class TestConnectionRequest(_message.Message):
    __slots__ = ("channel",)
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    channel: str
    def __init__(self, channel: _Optional[str] = ...) -> None: ...

class ConnectionResponse(_message.Message):
    __slots__ = ("id", "location", "channel", "provider", "config_preview", "created_at", "updated_at", "tested_at", "test_status")
    class ConfigPreviewEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CONFIG_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    TESTED_AT_FIELD_NUMBER: _ClassVar[int]
    TEST_STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    location: str
    channel: str
    provider: str
    config_preview: _containers.ScalarMap[str, str]
    created_at: str
    updated_at: str
    tested_at: str
    test_status: str
    def __init__(self, id: _Optional[str] = ..., location: _Optional[str] = ..., channel: _Optional[str] = ..., provider: _Optional[str] = ..., config_preview: _Optional[_Mapping[str, str]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., tested_at: _Optional[str] = ..., test_status: _Optional[str] = ...) -> None: ...

class ListConnectionsResponse(_message.Message):
    __slots__ = ("connections",)
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    connections: _containers.RepeatedCompositeFieldContainer[ConnectionResponse]
    def __init__(self, connections: _Optional[_Iterable[_Union[ConnectionResponse, _Mapping]]] = ...) -> None: ...

class DeleteConnectionResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class TestConnectionResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
