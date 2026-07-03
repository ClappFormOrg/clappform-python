from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.row import row_pb2 as _row_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Page(_message.Message):
    __slots__ = ("id", "slug", "name", "settings", "order", "group_id", "default_page", "rows", "created_at", "updated_at", "deleted_at", "versions")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PAGE_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    slug: str
    name: str
    settings: bytes
    order: int
    group_id: str
    default_page: bool
    rows: _containers.RepeatedCompositeFieldContainer[_row_pb2.Row]
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    def __init__(self, id: _Optional[str] = ..., slug: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ..., order: _Optional[int] = ..., group_id: _Optional[str] = ..., default_page: bool = ..., rows: _Optional[_Iterable[_Union[_row_pb2.Row, _Mapping]]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ...) -> None: ...

class PageRead(_message.Message):
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
    __slots__ = ("name", "settings", "order", "group_id", "default_page")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PAGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    settings: bytes
    order: int
    group_id: str
    default_page: bool
    def __init__(self, name: _Optional[str] = ..., settings: _Optional[bytes] = ..., order: _Optional[int] = ..., group_id: _Optional[str] = ..., default_page: bool = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "name", "settings", "order", "group_id", "default_page")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    settings: bytes
    order: int
    group_id: str
    default_page: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ..., order: _Optional[int] = ..., group_id: _Optional[str] = ..., default_page: bool = ...) -> None: ...

class Pages(_message.Message):
    __slots__ = ("pages", "rows", "pagination")
    PAGES_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pages: _containers.RepeatedCompositeFieldContainer[Page]
    rows: _containers.RepeatedCompositeFieldContainer[_row_pb2.Row]
    pagination: _commons_pb2.Pagination
    def __init__(self, pages: _Optional[_Iterable[_Union[Page, _Mapping]]] = ..., rows: _Optional[_Iterable[_Union[_row_pb2.Row, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
