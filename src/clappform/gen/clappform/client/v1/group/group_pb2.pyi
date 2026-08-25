from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.page import page_pb2 as _page_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Group(_message.Message):
    __slots__ = ("id", "name", "settings", "order", "pages", "app_id", "created_at", "updated_at", "deleted_at", "versions", "groups", "main_group_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    PAGES_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    MAIN_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    settings: bytes
    order: int
    pages: _containers.RepeatedCompositeFieldContainer[_page_pb2.Page]
    app_id: str
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    groups: _containers.RepeatedCompositeFieldContainer[Group]
    main_group_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ..., order: _Optional[int] = ..., pages: _Optional[_Iterable[_Union[_page_pb2.Page, _Mapping]]] = ..., app_id: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ..., groups: _Optional[_Iterable[_Union[Group, _Mapping]]] = ..., main_group_id: _Optional[str] = ...) -> None: ...

class GroupRead(_message.Message):
    __slots__ = ("group", "pages")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    PAGES_FIELD_NUMBER: _ClassVar[int]
    group: Group
    pages: _containers.RepeatedCompositeFieldContainer[_page_pb2.Page]
    def __init__(self, group: _Optional[_Union[Group, _Mapping]] = ..., pages: _Optional[_Iterable[_Union[_page_pb2.Page, _Mapping]]] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("name", "settings", "order", "app_id", "main_group_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    MAIN_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    settings: bytes
    order: int
    app_id: str
    main_group_id: str
    def __init__(self, name: _Optional[str] = ..., settings: _Optional[bytes] = ..., order: _Optional[int] = ..., app_id: _Optional[str] = ..., main_group_id: _Optional[str] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "name", "settings", "order", "main_group_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    MAIN_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    settings: bytes
    order: int
    main_group_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ..., order: _Optional[int] = ..., main_group_id: _Optional[str] = ...) -> None: ...

class Groups(_message.Message):
    __slots__ = ("groups", "pages", "pagination")
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    PAGES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[Group]
    pages: _containers.RepeatedCompositeFieldContainer[_page_pb2.Page]
    pagination: _commons_pb2.Pagination
    def __init__(self, groups: _Optional[_Iterable[_Union[Group, _Mapping]]] = ..., pages: _Optional[_Iterable[_Union[_page_pb2.Page, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
