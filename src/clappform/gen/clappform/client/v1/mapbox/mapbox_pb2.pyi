from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Style(_message.Message):
    __slots__ = ("id", "name", "version", "owner", "visibility", "protected", "created", "modified", "layers")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    PROTECTED_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    version: int
    owner: str
    visibility: str
    protected: bool
    created: str
    modified: str
    layers: _containers.RepeatedCompositeFieldContainer[StyleLayer]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., version: _Optional[int] = ..., owner: _Optional[str] = ..., visibility: _Optional[str] = ..., protected: bool = ..., created: _Optional[str] = ..., modified: _Optional[str] = ..., layers: _Optional[_Iterable[_Union[StyleLayer, _Mapping]]] = ...) -> None: ...

class StyleLayer(_message.Message):
    __slots__ = ("id", "type", "version", "minzoom", "maxzoom", "filter", "source", "source_layer", "layout", "paint", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MINZOOM_FIELD_NUMBER: _ClassVar[int]
    MAXZOOM_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_LAYER_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    PAINT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    version: int
    minzoom: float
    maxzoom: float
    filter: bytes
    source: str
    source_layer: str
    layout: bytes
    paint: bytes
    metadata: bytes
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., version: _Optional[int] = ..., minzoom: _Optional[float] = ..., maxzoom: _Optional[float] = ..., filter: _Optional[bytes] = ..., source: _Optional[str] = ..., source_layer: _Optional[str] = ..., layout: _Optional[bytes] = ..., paint: _Optional[bytes] = ..., metadata: _Optional[bytes] = ...) -> None: ...

class Styles(_message.Message):
    __slots__ = ("styles",)
    STYLES_FIELD_NUMBER: _ClassVar[int]
    styles: _containers.RepeatedCompositeFieldContainer[Style]
    def __init__(self, styles: _Optional[_Iterable[_Union[Style, _Mapping]]] = ...) -> None: ...

class Tileset(_message.Message):
    __slots__ = ("id", "name", "visibility", "center", "description", "filesize", "status", "created", "modified")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    CENTER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FILESIZE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    visibility: str
    center: _containers.RepeatedScalarFieldContainer[float]
    description: str
    filesize: int
    status: str
    created: str
    modified: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., visibility: _Optional[str] = ..., center: _Optional[_Iterable[float]] = ..., description: _Optional[str] = ..., filesize: _Optional[int] = ..., status: _Optional[str] = ..., created: _Optional[str] = ..., modified: _Optional[str] = ...) -> None: ...

class Tilesets(_message.Message):
    __slots__ = ("tilesets",)
    TILESETS_FIELD_NUMBER: _ClassVar[int]
    tilesets: _containers.RepeatedCompositeFieldContainer[Tileset]
    def __init__(self, tilesets: _Optional[_Iterable[_Union[Tileset, _Mapping]]] = ...) -> None: ...

class VectorLayer(_message.Message):
    __slots__ = ("id", "description", "minzoom", "maxzoom", "source", "source_name", "fields")
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MINZOOM_FIELD_NUMBER: _ClassVar[int]
    MAXZOOM_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    description: str
    minzoom: int
    maxzoom: int
    source: str
    source_name: str
    fields: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., description: _Optional[str] = ..., minzoom: _Optional[int] = ..., maxzoom: _Optional[int] = ..., source: _Optional[str] = ..., source_name: _Optional[str] = ..., fields: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TilesetMetadata(_message.Message):
    __slots__ = ("id", "name", "version", "type", "description", "filesize", "minzoom", "maxzoom", "bounds", "center", "created", "modified", "vector_layers")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FILESIZE_FIELD_NUMBER: _ClassVar[int]
    MINZOOM_FIELD_NUMBER: _ClassVar[int]
    MAXZOOM_FIELD_NUMBER: _ClassVar[int]
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    CENTER_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    VECTOR_LAYERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    version: str
    type: str
    description: str
    filesize: int
    minzoom: int
    maxzoom: int
    bounds: _containers.RepeatedScalarFieldContainer[float]
    center: _containers.RepeatedScalarFieldContainer[float]
    created: int
    modified: int
    vector_layers: _containers.RepeatedCompositeFieldContainer[VectorLayer]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., version: _Optional[str] = ..., type: _Optional[str] = ..., description: _Optional[str] = ..., filesize: _Optional[int] = ..., minzoom: _Optional[int] = ..., maxzoom: _Optional[int] = ..., bounds: _Optional[_Iterable[float]] = ..., center: _Optional[_Iterable[float]] = ..., created: _Optional[int] = ..., modified: _Optional[int] = ..., vector_layers: _Optional[_Iterable[_Union[VectorLayer, _Mapping]]] = ...) -> None: ...
