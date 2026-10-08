from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.authoriser.v1.password import password_pb2 as _password_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AzureAuthorities(_message.Message):
    __slots__ = ("authorities", "pagination")
    AUTHORITIES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    authorities: _containers.RepeatedCompositeFieldContainer[AzureAuthority]
    pagination: _commons_pb2.Pagination
    def __init__(self, authorities: _Optional[_Iterable[_Union[AzureAuthority, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...

class AzureAuthority(_message.Message):
    __slots__ = ("id", "authority", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    authority: str
    type: str
    def __init__(self, id: _Optional[str] = ..., authority: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class AzureAuthRequest(_message.Message):
    __slots__ = ("authority", "code_challenge", "state")
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    CODE_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    authority: str
    code_challenge: str
    state: str
    def __init__(self, authority: _Optional[str] = ..., code_challenge: _Optional[str] = ..., state: _Optional[str] = ...) -> None: ...

class AzureAuthResponse(_message.Message):
    __slots__ = ("redirect_url", "set_cookie")
    REDIRECT_URL_FIELD_NUMBER: _ClassVar[int]
    SET_COOKIE_FIELD_NUMBER: _ClassVar[int]
    redirect_url: str
    set_cookie: str
    def __init__(self, redirect_url: _Optional[str] = ..., set_cookie: _Optional[str] = ...) -> None: ...

class AzureAuthACSRequest(_message.Message):
    __slots__ = ("SAMLResponse", "authority")
    SAMLRESPONSE_FIELD_NUMBER: _ClassVar[int]
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    SAMLResponse: bytes
    authority: str
    def __init__(self, SAMLResponse: _Optional[bytes] = ..., authority: _Optional[str] = ...) -> None: ...

class AzureAuthOAuthACSRequest(_message.Message):
    __slots__ = ("code", "authority", "code_challenge")
    CODE_FIELD_NUMBER: _ClassVar[int]
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    CODE_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    code: str
    authority: str
    code_challenge: str
    def __init__(self, code: _Optional[str] = ..., authority: _Optional[str] = ..., code_challenge: _Optional[str] = ...) -> None: ...

class AuthIdRequest(_message.Message):
    __slots__ = ("user_uuid",)
    USER_UUID_FIELD_NUMBER: _ClassVar[int]
    user_uuid: str
    def __init__(self, user_uuid: _Optional[str] = ...) -> None: ...
