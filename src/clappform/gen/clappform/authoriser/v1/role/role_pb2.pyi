from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.authoriser.v1.permission import permission_pb2 as _permission_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Role(_message.Message):
    __slots__ = ("id", "name", "users", "permissions", "created_at", "updated_at", "deleted_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    users: _containers.RepeatedScalarFieldContainer[str]
    permissions: _containers.RepeatedCompositeFieldContainer[_permission_pb2.Permission]
    created_at: str
    updated_at: str
    deleted_at: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., users: _Optional[_Iterable[str]] = ..., permissions: _Optional[_Iterable[_Union[_permission_pb2.Permission, _Mapping]]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("name", "users", "permissions")
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    users: _containers.RepeatedScalarFieldContainer[str]
    permissions: _containers.RepeatedCompositeFieldContainer[_permission_pb2.Permission]
    def __init__(self, name: _Optional[str] = ..., users: _Optional[_Iterable[str]] = ..., permissions: _Optional[_Iterable[_Union[_permission_pb2.Permission, _Mapping]]] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "name", "users", "permissions")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    users: _containers.RepeatedScalarFieldContainer[str]
    permissions: _containers.RepeatedCompositeFieldContainer[_permission_pb2.Permission]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., users: _Optional[_Iterable[str]] = ..., permissions: _Optional[_Iterable[_Union[_permission_pb2.Permission, _Mapping]]] = ...) -> None: ...

class Roles(_message.Message):
    __slots__ = ("roles", "pagination")
    ROLES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    roles: _containers.RepeatedCompositeFieldContainer[Role]
    pagination: _commons_pb2.Pagination
    def __init__(self, roles: _Optional[_Iterable[_Union[Role, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
