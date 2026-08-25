from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Authorities(_message.Message):
    __slots__ = ("authorities", "pagination")
    AUTHORITIES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    authorities: _containers.RepeatedCompositeFieldContainer[Authority]
    pagination: _commons_pb2.Pagination
    def __init__(self, authorities: _Optional[_Iterable[_Union[Authority, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...

class CreateProfile(_message.Message):
    __slots__ = ("authority", "client_id", "app_id", "type", "certificate", "private_key", "webhook_secret", "default_roles", "auto_initiate", "default_user_info")
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_SECRET_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ROLES_FIELD_NUMBER: _ClassVar[int]
    AUTO_INITIATE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    authority: str
    client_id: str
    app_id: str
    type: str
    certificate: bytes
    private_key: bytes
    webhook_secret: bytes
    default_roles: _containers.RepeatedScalarFieldContainer[str]
    auto_initiate: bool
    default_user_info: bytes
    def __init__(self, authority: _Optional[str] = ..., client_id: _Optional[str] = ..., app_id: _Optional[str] = ..., type: _Optional[str] = ..., certificate: _Optional[bytes] = ..., private_key: _Optional[bytes] = ..., webhook_secret: _Optional[bytes] = ..., default_roles: _Optional[_Iterable[str]] = ..., auto_initiate: bool = ..., default_user_info: _Optional[bytes] = ...) -> None: ...

class UpdateProfile(_message.Message):
    __slots__ = ("authority", "app_id", "certificate", "private_key", "webhook_secret", "default_roles", "auto_initiate", "default_user_info")
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_SECRET_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ROLES_FIELD_NUMBER: _ClassVar[int]
    AUTO_INITIATE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_USER_INFO_FIELD_NUMBER: _ClassVar[int]
    authority: str
    app_id: str
    certificate: bytes
    private_key: bytes
    webhook_secret: bytes
    default_roles: _containers.RepeatedScalarFieldContainer[str]
    auto_initiate: bool
    default_user_info: bytes
    def __init__(self, authority: _Optional[str] = ..., app_id: _Optional[str] = ..., certificate: _Optional[bytes] = ..., private_key: _Optional[bytes] = ..., webhook_secret: _Optional[bytes] = ..., default_roles: _Optional[_Iterable[str]] = ..., auto_initiate: bool = ..., default_user_info: _Optional[bytes] = ...) -> None: ...

class Authority(_message.Message):
    __slots__ = ("id", "authority", "type", "auto_initiate")
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTO_INITIATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    authority: str
    type: str
    auto_initiate: bool
    def __init__(self, id: _Optional[str] = ..., authority: _Optional[str] = ..., type: _Optional[str] = ..., auto_initiate: bool = ...) -> None: ...
