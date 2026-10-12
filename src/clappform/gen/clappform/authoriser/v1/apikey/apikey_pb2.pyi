from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.authoriser.v1.user import user_pb2 as _user_pb2
from clappform.gen.clappform.authoriser.v1.permission import permission_pb2 as _permission_pb2
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class APIKeys(_message.Message):
    __slots__ = ("api_keys", "pagination")
    API_KEYS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    api_keys: _containers.RepeatedCompositeFieldContainer[APIKey]
    pagination: _commons_pb2.Pagination
    def __init__(self, api_keys: _Optional[_Iterable[_Union[APIKey, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...

class APIKey(_message.Message):
    __slots__ = ("id", "name", "api_key", "expiration_date", "user_id", "permissions", "created_at", "deleted_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    api_key: str
    expiration_date: str
    user_id: str
    permissions: _containers.RepeatedCompositeFieldContainer[_permission_pb2.Permission]
    created_at: str
    deleted_at: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., api_key: _Optional[str] = ..., expiration_date: _Optional[str] = ..., user_id: _Optional[str] = ..., permissions: _Optional[_Iterable[_Union[_permission_pb2.Permission, _Mapping]]] = ..., created_at: _Optional[str] = ..., deleted_at: _Optional[str] = ...) -> None: ...

class GenerateKeyRequest(_message.Message):
    __slots__ = ("name", "expiration_date", "permissions")
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    expiration_date: int
    permissions: _containers.RepeatedCompositeFieldContainer[_permission_pb2.Permission]
    def __init__(self, name: _Optional[str] = ..., expiration_date: _Optional[int] = ..., permissions: _Optional[_Iterable[_Union[_permission_pb2.Permission, _Mapping]]] = ...) -> None: ...

class VerifyKeyRequest(_message.Message):
    __slots__ = ("api_key",)
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    def __init__(self, api_key: _Optional[str] = ...) -> None: ...

class VerifyKeyResponse(_message.Message):
    __slots__ = ("user", "client", "permissions")
    USER_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    user: _user_pb2.User
    client: str
    permissions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, user: _Optional[_Union[_user_pb2.User, _Mapping]] = ..., client: _Optional[str] = ..., permissions: _Optional[_Iterable[str]] = ...) -> None: ...
