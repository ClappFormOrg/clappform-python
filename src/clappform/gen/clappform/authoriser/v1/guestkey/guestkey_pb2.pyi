from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.authoriser.v1.password import password_pb2 as _password_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AuthRequest(_message.Message):
    __slots__ = ("deep_dive", "permissions")
    DEEP_DIVE_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    deep_dive: bytes
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, deep_dive: _Optional[bytes] = ..., permissions: _Optional[_Iterable[str]] = ...) -> None: ...
