from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SupportedDatabases(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[SupportedDatabases]
    MONGO: _ClassVar[SupportedDatabases]
    DATALAKE: _ClassVar[SupportedDatabases]
    ELASTIC: _ClassVar[SupportedDatabases]
    RELATIONAL: _ClassVar[SupportedDatabases]
    DATALAKE_ELASTIC: _ClassVar[SupportedDatabases]
UNSPECIFIED: SupportedDatabases
MONGO: SupportedDatabases
DATALAKE: SupportedDatabases
ELASTIC: SupportedDatabases
RELATIONAL: SupportedDatabases
DATALAKE_ELASTIC: SupportedDatabases

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LandingPage(_message.Message):
    __slots__ = ("title", "description", "links")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    links: _containers.RepeatedCompositeFieldContainer[Link]
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., links: _Optional[_Iterable[_Union[Link, _Mapping]]] = ...) -> None: ...

class Link(_message.Message):
    __slots__ = ("href", "rel", "type", "title")
    HREF_FIELD_NUMBER: _ClassVar[int]
    REL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    href: str
    rel: str
    type: str
    title: str
    def __init__(self, href: _Optional[str] = ..., rel: _Optional[str] = ..., type: _Optional[str] = ..., title: _Optional[str] = ...) -> None: ...
