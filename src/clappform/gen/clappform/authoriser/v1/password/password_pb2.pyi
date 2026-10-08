from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.authoriser.v1.user import user_pb2 as _user_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthRequest(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class DeauthResponse(_message.Message):
    __slots__ = ("message", "set_cookie")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SET_COOKIE_FIELD_NUMBER: _ClassVar[int]
    message: str
    set_cookie: str
    def __init__(self, message: _Optional[str] = ..., set_cookie: _Optional[str] = ...) -> None: ...

class RefreshTokenRequest(_message.Message):
    __slots__ = ("refresh_token",)
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    refresh_token: str
    def __init__(self, refresh_token: _Optional[str] = ...) -> None: ...

class AuthTokenRequest(_message.Message):
    __slots__ = ("authorization_token", "detail_level")
    AUTHORIZATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DETAIL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    authorization_token: str
    detail_level: int
    def __init__(self, authorization_token: _Optional[str] = ..., detail_level: _Optional[int] = ...) -> None: ...

class AuthTokenResponse(_message.Message):
    __slots__ = ("authorization_token", "refresh_token", "otp_required", "validation_key", "user_id")
    AUTHORIZATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    OTP_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_KEY_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    authorization_token: str
    refresh_token: str
    otp_required: bool
    validation_key: str
    user_id: str
    def __init__(self, authorization_token: _Optional[str] = ..., refresh_token: _Optional[str] = ..., otp_required: bool = ..., validation_key: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class AuthUserResponse(_message.Message):
    __slots__ = ("user", "client", "permissions", "external_token")
    USER_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_TOKEN_FIELD_NUMBER: _ClassVar[int]
    user: _user_pb2.User
    client: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    external_token: bool
    def __init__(self, user: _Optional[_Union[_user_pb2.User, _Mapping]] = ..., client: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ..., external_token: bool = ...) -> None: ...
