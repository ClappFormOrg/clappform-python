from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Users(_message.Message):
    __slots__ = ("users", "pagination")
    USERS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    pagination: _commons_pb2.Pagination
    def __init__(self, users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "email", "first_name", "last_name", "is_active", "last_online", "extra_information", "otp_enabled", "created_at", "updated_at", "deleted_at", "roles", "preferences")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    LAST_ONLINE_FIELD_NUMBER: _ClassVar[int]
    EXTRA_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    OTP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    last_online: str
    extra_information: bytes
    otp_enabled: bool
    created_at: str
    updated_at: str
    deleted_at: str
    roles: _containers.RepeatedScalarFieldContainer[str]
    preferences: bytes
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., is_active: bool = ..., last_online: _Optional[str] = ..., extra_information: _Optional[bytes] = ..., otp_enabled: bool = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., roles: _Optional[_Iterable[str]] = ..., preferences: _Optional[bytes] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("email", "first_name", "last_name", "password", "is_active", "extra_information", "roles", "preferences")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    EXTRA_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    email: str
    first_name: str
    last_name: str
    password: str
    is_active: bool
    extra_information: bytes
    roles: _containers.RepeatedScalarFieldContainer[str]
    preferences: bytes
    def __init__(self, email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., password: _Optional[str] = ..., is_active: bool = ..., extra_information: _Optional[bytes] = ..., roles: _Optional[_Iterable[str]] = ..., preferences: _Optional[bytes] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "email", "first_name", "last_name", "password", "extra_information", "roles", "preferences")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    EXTRA_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    first_name: str
    last_name: str
    password: str
    extra_information: bytes
    roles: _containers.RepeatedScalarFieldContainer[str]
    preferences: bytes
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., password: _Optional[str] = ..., extra_information: _Optional[bytes] = ..., roles: _Optional[_Iterable[str]] = ..., preferences: _Optional[bytes] = ...) -> None: ...
