from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from clappform.gen.clappform.client.v1.collection import collection_pb2 as _collection_pb2
from clappform.gen.clappform.client.v1.page import page_pb2 as _page_pb2
from clappform.gen.clappform.client.v1.group import group_pb2 as _group_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tag(_message.Message):
    __slots__ = ("id", "color", "icon")
    ID_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    id: str
    color: str
    icon: str
    def __init__(self, id: _Optional[str] = ..., color: _Optional[str] = ..., icon: _Optional[str] = ...) -> None: ...

class App(_message.Message):
    __slots__ = ("id", "slug", "settings", "tags", "default_page", "groups", "collections", "created_at", "updated_at", "deleted_at", "versions")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PAGE_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    slug: str
    settings: bytes
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    default_page: _page_pb2.Page
    groups: _containers.RepeatedCompositeFieldContainer[_group_pb2.Group]
    collections: _containers.RepeatedCompositeFieldContainer[_collection_pb2.Collection]
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    def __init__(self, id: _Optional[str] = ..., slug: _Optional[str] = ..., settings: _Optional[bytes] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ..., default_page: _Optional[_Union[_page_pb2.Page, _Mapping]] = ..., groups: _Optional[_Iterable[_Union[_group_pb2.Group, _Mapping]]] = ..., collections: _Optional[_Iterable[_Union[_collection_pb2.Collection, _Mapping]]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("slug", "settings", "tags")
    SLUG_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    slug: str
    settings: bytes
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, slug: _Optional[str] = ..., settings: _Optional[bytes] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "slug", "settings", "tags")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    slug: str
    settings: bytes
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    def __init__(self, id: _Optional[str] = ..., slug: _Optional[str] = ..., settings: _Optional[bytes] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ...) -> None: ...

class Apps(_message.Message):
    __slots__ = ("apps", "pagination")
    APPS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    apps: _containers.RepeatedCompositeFieldContainer[App]
    pagination: _commons_pb2.Pagination
    def __init__(self, apps: _Optional[_Iterable[_Union[App, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
