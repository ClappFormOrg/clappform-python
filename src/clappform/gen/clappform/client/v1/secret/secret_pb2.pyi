from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Scope(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_SCOPE: _ClassVar[Scope]
    SYSTEM: _ClassVar[Scope]
    DATABASE: _ClassVar[Scope]
    EXTERNAL_API: _ClassVar[Scope]
    FILE_STORAGE: _ClassVar[Scope]
    FTP: _ClassVar[Scope]
    DASHBOARD: _ClassVar[Scope]
    PERSONAL: _ClassVar[Scope]
    OTHER_SCOPE: _ClassVar[Scope]

class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_TYPE: _ClassVar[Type]
    DICT: _ClassVar[Type]
    LIST: _ClassVar[Type]
    STRING: _ClassVar[Type]
    NUMBER: _ClassVar[Type]
    BYTES: _ClassVar[Type]
    FILE: _ClassVar[Type]
    BOOL: _ClassVar[Type]
    AUTH_BEARER: _ClassVar[Type]
    AUTH_API_KEY: _ClassVar[Type]
    AUTH_BASIC: _ClassVar[Type]
    AUTH_OAUTH: _ClassVar[Type]
    SFTP: _ClassVar[Type]
    AZURE_FILE_SAS: _ClassVar[Type]
    AZURE_FILE_CONN_STRING: _ClassVar[Type]
    OTHER_TYPE: _ClassVar[Type]
UNSPECIFIED_SCOPE: Scope
SYSTEM: Scope
DATABASE: Scope
EXTERNAL_API: Scope
FILE_STORAGE: Scope
FTP: Scope
DASHBOARD: Scope
PERSONAL: Scope
OTHER_SCOPE: Scope
UNSPECIFIED_TYPE: Type
DICT: Type
LIST: Type
STRING: Type
NUMBER: Type
BYTES: Type
FILE: Type
BOOL: Type
AUTH_BEARER: Type
AUTH_API_KEY: Type
AUTH_BASIC: Type
AUTH_OAUTH: Type
SFTP: Type
AZURE_FILE_SAS: Type
AZURE_FILE_CONN_STRING: Type
OTHER_TYPE: Type

class Secret(_message.Message):
    __slots__ = ("id", "key", "value", "encrypted", "scope", "type", "created_by", "updated_by", "expires_at", "expires_at_iso", "expired", "ttl_days", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_ISO_FIELD_NUMBER: _ClassVar[int]
    EXPIRED_FIELD_NUMBER: _ClassVar[int]
    TTL_DAYS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    key: str
    value: bytes
    encrypted: bool
    scope: str
    type: str
    created_by: str
    updated_by: str
    expires_at: int
    expires_at_iso: str
    expired: bool
    ttl_days: int
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., key: _Optional[str] = ..., value: _Optional[bytes] = ..., encrypted: bool = ..., scope: _Optional[str] = ..., type: _Optional[str] = ..., created_by: _Optional[str] = ..., updated_by: _Optional[str] = ..., expires_at: _Optional[int] = ..., expires_at_iso: _Optional[str] = ..., expired: bool = ..., ttl_days: _Optional[int] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("key", "value", "encrypted", "scope", "type", "expires_at")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: bytes
    encrypted: bool
    scope: Scope
    type: Type
    expires_at: int
    def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ..., encrypted: bool = ..., scope: _Optional[_Union[Scope, str]] = ..., type: _Optional[_Union[Type, str]] = ..., expires_at: _Optional[int] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("key", "scope", "value", "type", "encrypted", "expires_at")
    KEY_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    key: str
    scope: Scope
    value: bytes
    type: Type
    encrypted: bool
    expires_at: int
    def __init__(self, key: _Optional[str] = ..., scope: _Optional[_Union[Scope, str]] = ..., value: _Optional[bytes] = ..., type: _Optional[_Union[Type, str]] = ..., encrypted: bool = ..., expires_at: _Optional[int] = ...) -> None: ...

class Secrets(_message.Message):
    __slots__ = ("secrets", "pagination")
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    secrets: _containers.RepeatedCompositeFieldContainer[Secret]
    pagination: _commons_pb2.Pagination
    def __init__(self, secrets: _Optional[_Iterable[_Union[Secret, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...

class SecretRead(_message.Message):
    __slots__ = ("key", "scope")
    KEY_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    key: str
    scope: Scope
    def __init__(self, key: _Optional[str] = ..., scope: _Optional[_Union[Scope, str]] = ...) -> None: ...
