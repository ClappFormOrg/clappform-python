from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class databaseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[databaseType]
    MONGO: _ClassVar[databaseType]
    POSTGRES: _ClassVar[databaseType]
    DATALAKE: _ClassVar[databaseType]
    RELATIONAL: _ClassVar[databaseType]
    ELASTIC: _ClassVar[databaseType]
    DATALAKE_ELASTIC: _ClassVar[databaseType]
    VIEW_MONGO: _ClassVar[databaseType]
UNSPECIFIED: databaseType
MONGO: databaseType
POSTGRES: databaseType
DATALAKE: databaseType
RELATIONAL: databaseType
ELASTIC: databaseType
DATALAKE_ELASTIC: databaseType
VIEW_MONGO: databaseType

class Collection(_message.Message):
    __slots__ = ("id", "slug", "settings", "app_id", "database", "created_at", "updated_at", "deleted_at", "versions", "collection_rules")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_RULES_FIELD_NUMBER: _ClassVar[int]
    id: str
    slug: str
    settings: bytes
    app_id: str
    database: str
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    collection_rules: _containers.RepeatedCompositeFieldContainer[CollectionRule]
    def __init__(self, id: _Optional[str] = ..., slug: _Optional[str] = ..., settings: _Optional[bytes] = ..., app_id: _Optional[str] = ..., database: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ..., collection_rules: _Optional[_Iterable[_Union[CollectionRule, _Mapping]]] = ...) -> None: ...

class CollectionRead(_message.Message):
    __slots__ = ("id", "detail_level", "include_deleted", "app")
    ID_FIELD_NUMBER: _ClassVar[int]
    DETAIL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    id: str
    detail_level: int
    include_deleted: bool
    app: str
    def __init__(self, id: _Optional[str] = ..., detail_level: _Optional[int] = ..., include_deleted: bool = ..., app: _Optional[str] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("slug", "settings", "app_id", "database")
    SLUG_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    slug: str
    settings: bytes
    app_id: str
    database: databaseType
    def __init__(self, slug: _Optional[str] = ..., settings: _Optional[bytes] = ..., app_id: _Optional[str] = ..., database: _Optional[_Union[databaseType, str]] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "settings", "slug")
    ID_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    id: str
    settings: bytes
    slug: str
    def __init__(self, id: _Optional[str] = ..., settings: _Optional[bytes] = ..., slug: _Optional[str] = ...) -> None: ...

class Collections(_message.Message):
    __slots__ = ("collections", "pagination")
    COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    collections: _containers.RepeatedCompositeFieldContainer[Collection]
    pagination: _commons_pb2.Pagination
    def __init__(self, collections: _Optional[_Iterable[_Union[Collection, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...

class CollectionRule(_message.Message):
    __slots__ = ("id", "name", "settings")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    settings: bytes
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ...) -> None: ...
