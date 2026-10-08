from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueriedAddress(_message.Message):
    __slots__ = ("postal_code", "house_number")
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    HOUSE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    postal_code: str
    house_number: str
    def __init__(self, postal_code: _Optional[str] = ..., house_number: _Optional[str] = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ("type", "coordinates")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    type: str
    coordinates: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, type: _Optional[str] = ..., coordinates: _Optional[_Iterable[float]] = ...) -> None: ...

class Address(_message.Message):
    __slots__ = ("postcode", "number", "street", "city", "municipality", "province", "location")
    POSTCODE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    STREET_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    MUNICIPALITY_FIELD_NUMBER: _ClassVar[int]
    PROVINCE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    postcode: str
    number: int
    street: str
    city: str
    municipality: str
    province: str
    location: Location
    def __init__(self, postcode: _Optional[str] = ..., number: _Optional[int] = ..., street: _Optional[str] = ..., city: _Optional[str] = ..., municipality: _Optional[str] = ..., province: _Optional[str] = ..., location: _Optional[_Union[Location, _Mapping]] = ...) -> None: ...
