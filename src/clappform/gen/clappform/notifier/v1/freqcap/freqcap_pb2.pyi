from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChannelCapRule(_message.Message):
    __slots__ = ("channel", "max_per_hour", "max_per_day")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    MAX_PER_HOUR_FIELD_NUMBER: _ClassVar[int]
    MAX_PER_DAY_FIELD_NUMBER: _ClassVar[int]
    channel: str
    max_per_hour: int
    max_per_day: int
    def __init__(self, channel: _Optional[str] = ..., max_per_hour: _Optional[int] = ..., max_per_day: _Optional[int] = ...) -> None: ...

class FreqCapRules(_message.Message):
    __slots__ = ("rules", "priority_overrides")
    class PriorityOverridesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    RULES_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[ChannelCapRule]
    priority_overrides: _containers.ScalarMap[str, str]
    def __init__(self, rules: _Optional[_Iterable[_Union[ChannelCapRule, _Mapping]]] = ..., priority_overrides: _Optional[_Mapping[str, str]] = ...) -> None: ...

class GetFreqCapRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpsertFreqCapResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class GetFreqCapResponse(_message.Message):
    __slots__ = ("rules", "priority_overrides")
    class PriorityOverridesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    RULES_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[ChannelCapRule]
    priority_overrides: _containers.ScalarMap[str, str]
    def __init__(self, rules: _Optional[_Iterable[_Union[ChannelCapRule, _Mapping]]] = ..., priority_overrides: _Optional[_Mapping[str, str]] = ...) -> None: ...
