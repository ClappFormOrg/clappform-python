from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GenerateResponse(_message.Message):
    __slots__ = ("secret", "url", "qr_code")
    SECRET_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    QR_CODE_FIELD_NUMBER: _ClassVar[int]
    secret: str
    url: str
    qr_code: bytes
    def __init__(self, secret: _Optional[str] = ..., url: _Optional[str] = ..., qr_code: _Optional[bytes] = ...) -> None: ...

class TokenRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class VerifyResponse(_message.Message):
    __slots__ = ("message", "recovery_codes")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RECOVERY_CODES_FIELD_NUMBER: _ClassVar[int]
    message: str
    recovery_codes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, message: _Optional[str] = ..., recovery_codes: _Optional[_Iterable[str]] = ...) -> None: ...

class ValidateRequest(_message.Message):
    __slots__ = ("input_token", "validation_key")
    INPUT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_KEY_FIELD_NUMBER: _ClassVar[int]
    input_token: str
    validation_key: str
    def __init__(self, input_token: _Optional[str] = ..., validation_key: _Optional[str] = ...) -> None: ...

class ValidateResponse(_message.Message):
    __slots__ = ("valid", "authorization_token", "refresh_token", "user_id")
    VALID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    authorization_token: str
    refresh_token: str
    user_id: str
    def __init__(self, valid: bool = ..., authorization_token: _Optional[str] = ..., refresh_token: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class RecoverRequest(_message.Message):
    __slots__ = ("token", "username")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    token: str
    username: str
    def __init__(self, token: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class RecoverResponse(_message.Message):
    __slots__ = ("valid", "authorization_token", "refresh_token")
    VALID_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    authorization_token: str
    refresh_token: str
    def __init__(self, valid: bool = ..., authorization_token: _Optional[str] = ..., refresh_token: _Optional[str] = ...) -> None: ...
