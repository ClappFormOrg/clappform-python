from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.widget import widget_pb2 as _widget_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Row(_message.Message):
    __slots__ = ("id", "slug", "settings", "order", "page_id", "widgets", "created_at", "updated_at", "deleted_at", "versions")
    ID_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    PAGE_ID_FIELD_NUMBER: _ClassVar[int]
    WIDGETS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    slug: str
    settings: bytes
    order: int
    page_id: str
    widgets: _containers.RepeatedCompositeFieldContainer[_widget_pb2.Widget]
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    def __init__(self, id: _Optional[str] = ..., slug: _Optional[str] = ..., settings: _Optional[bytes] = ..., order: _Optional[int] = ..., page_id: _Optional[str] = ..., widgets: _Optional[_Iterable[_Union[_widget_pb2.Widget, _Mapping]]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ...) -> None: ...

class RowRead(_message.Message):
    __slots__ = ("row", "widgets")
    ROW_FIELD_NUMBER: _ClassVar[int]
    WIDGETS_FIELD_NUMBER: _ClassVar[int]
    row: Row
    widgets: _containers.RepeatedCompositeFieldContainer[_widget_pb2.Widget]
    def __init__(self, row: _Optional[_Union[Row, _Mapping]] = ..., widgets: _Optional[_Iterable[_Union[_widget_pb2.Widget, _Mapping]]] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("settings", "order", "page_id")
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    PAGE_ID_FIELD_NUMBER: _ClassVar[int]
    settings: bytes
    order: int
    page_id: str
    def __init__(self, settings: _Optional[bytes] = ..., order: _Optional[int] = ..., page_id: _Optional[str] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "settings", "order", "page_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    PAGE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    settings: bytes
    order: int
    page_id: str
    def __init__(self, id: _Optional[str] = ..., settings: _Optional[bytes] = ..., order: _Optional[int] = ..., page_id: _Optional[str] = ...) -> None: ...

class Rows(_message.Message):
    __slots__ = ("rows", "widgets", "pagination")
    ROWS_FIELD_NUMBER: _ClassVar[int]
    WIDGETS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[Row]
    widgets: _containers.RepeatedCompositeFieldContainer[_widget_pb2.Widget]
    pagination: _commons_pb2.Pagination
    def __init__(self, rows: _Optional[_Iterable[_Union[Row, _Mapping]]] = ..., widgets: _Optional[_Iterable[_Union[_widget_pb2.Widget, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
