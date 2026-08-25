from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.version import version_pb2 as _version_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Widget(_message.Message):
    __slots__ = ("id", "name", "settings", "main_widget_id", "created_at", "updated_at", "deleted_at", "versions", "drill_down_widgets", "main_change_id", "change_widgets")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    MAIN_WIDGET_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    DRILL_DOWN_WIDGETS_FIELD_NUMBER: _ClassVar[int]
    MAIN_CHANGE_ID_FIELD_NUMBER: _ClassVar[int]
    CHANGE_WIDGETS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    settings: bytes
    main_widget_id: str
    created_at: str
    updated_at: str
    deleted_at: str
    versions: _containers.RepeatedCompositeFieldContainer[_version_pb2.Version]
    drill_down_widgets: _containers.RepeatedCompositeFieldContainer[Widget]
    main_change_id: str
    change_widgets: _containers.RepeatedCompositeFieldContainer[Widget]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ..., main_widget_id: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., versions: _Optional[_Iterable[_Union[_version_pb2.Version, _Mapping]]] = ..., drill_down_widgets: _Optional[_Iterable[_Union[Widget, _Mapping]]] = ..., main_change_id: _Optional[str] = ..., change_widgets: _Optional[_Iterable[_Union[Widget, _Mapping]]] = ...) -> None: ...

class CreateRequest(_message.Message):
    __slots__ = ("name", "settings", "row_id", "main_widget_id", "main_change_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ROW_ID_FIELD_NUMBER: _ClassVar[int]
    MAIN_WIDGET_ID_FIELD_NUMBER: _ClassVar[int]
    MAIN_CHANGE_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    settings: bytes
    row_id: str
    main_widget_id: str
    main_change_id: str
    def __init__(self, name: _Optional[str] = ..., settings: _Optional[bytes] = ..., row_id: _Optional[str] = ..., main_widget_id: _Optional[str] = ..., main_change_id: _Optional[str] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("id", "name", "settings", "row_id", "main_widget_id", "main_change_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ROW_ID_FIELD_NUMBER: _ClassVar[int]
    MAIN_WIDGET_ID_FIELD_NUMBER: _ClassVar[int]
    MAIN_CHANGE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    settings: bytes
    row_id: str
    main_widget_id: str
    main_change_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., settings: _Optional[bytes] = ..., row_id: _Optional[str] = ..., main_widget_id: _Optional[str] = ..., main_change_id: _Optional[str] = ...) -> None: ...

class Widgets(_message.Message):
    __slots__ = ("widgets", "pagination")
    WIDGETS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    widgets: _containers.RepeatedCompositeFieldContainer[Widget]
    pagination: _commons_pb2.Pagination
    def __init__(self, widgets: _Optional[_Iterable[_Union[Widget, _Mapping]]] = ..., pagination: _Optional[_Union[_commons_pb2.Pagination, _Mapping]] = ...) -> None: ...
