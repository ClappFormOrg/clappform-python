from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[status]
    OK: _ClassVar[status]
    UNAVAILABLE: _ClassVar[status]
    MAINTENANCE: _ClassVar[status]
    ERROR: _ClassVar[status]
UNSPECIFIED: status
OK: status
UNAVAILABLE: status
MAINTENANCE: status
ERROR: status

class HealthStatus(_message.Message):
    __slots__ = ("service", "status", "timestamp")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    service: str
    status: status
    timestamp: str
    def __init__(self, service: _Optional[str] = ..., status: _Optional[_Union[status, str]] = ..., timestamp: _Optional[str] = ...) -> None: ...
