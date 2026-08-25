from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChannelAvailability(_message.Message):
    __slots__ = ("always", "business_hours_only", "timezone")
    ALWAYS_FIELD_NUMBER: _ClassVar[int]
    BUSINESS_HOURS_ONLY_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    always: bool
    business_hours_only: bool
    timezone: str
    def __init__(self, always: bool = ..., business_hours_only: bool = ..., timezone: _Optional[str] = ...) -> None: ...

class QuietHours(_message.Message):
    __slots__ = ("enabled", "start", "end", "timezone", "override_for_priority")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FOR_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    start: str
    end: str
    timezone: str
    override_for_priority: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, enabled: bool = ..., start: _Optional[str] = ..., end: _Optional[str] = ..., timezone: _Optional[str] = ..., override_for_priority: _Optional[_Iterable[str]] = ...) -> None: ...

class UserPreferences(_message.Message):
    __slots__ = ("user_id", "preferred_channels", "channel_availability", "quiet_hours")
    class ChannelAvailabilityEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ChannelAvailability
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ChannelAvailability, _Mapping]] = ...) -> None: ...
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    QUIET_HOURS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    preferred_channels: _containers.RepeatedScalarFieldContainer[str]
    channel_availability: _containers.MessageMap[str, ChannelAvailability]
    quiet_hours: QuietHours
    def __init__(self, user_id: _Optional[str] = ..., preferred_channels: _Optional[_Iterable[str]] = ..., channel_availability: _Optional[_Mapping[str, ChannelAvailability]] = ..., quiet_hours: _Optional[_Union[QuietHours, _Mapping]] = ...) -> None: ...

class GetPreferencesRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class DeletePreferencesRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...
