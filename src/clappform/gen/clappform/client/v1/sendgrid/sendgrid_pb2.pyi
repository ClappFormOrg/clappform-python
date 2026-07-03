from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Recipient(_message.Message):
    __slots__ = ("email", "name")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class Personalization(_message.Message):
    __slots__ = ("to", "bcc", "dynamic_template_data", "attachments")
    TO_FIELD_NUMBER: _ClassVar[int]
    BCC_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_TEMPLATE_DATA_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    to: _containers.RepeatedCompositeFieldContainer[Recipient]
    bcc: _containers.RepeatedCompositeFieldContainer[Recipient]
    dynamic_template_data: bytes
    attachments: _containers.RepeatedCompositeFieldContainer[Attachment]
    def __init__(self, to: _Optional[_Iterable[_Union[Recipient, _Mapping]]] = ..., bcc: _Optional[_Iterable[_Union[Recipient, _Mapping]]] = ..., dynamic_template_data: _Optional[bytes] = ..., attachments: _Optional[_Iterable[_Union[Attachment, _Mapping]]] = ...) -> None: ...

class Attachment(_message.Message):
    __slots__ = ("content", "type", "filename", "disposition")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    DISPOSITION_FIELD_NUMBER: _ClassVar[int]
    content: str
    type: str
    filename: str
    disposition: str
    def __init__(self, content: _Optional[str] = ..., type: _Optional[str] = ..., filename: _Optional[str] = ..., disposition: _Optional[str] = ...) -> None: ...

class EmailRequest(_message.Message):
    __slots__ = ("template_id", "personalizations", "include_tracking")
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    PERSONALIZATIONS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TRACKING_FIELD_NUMBER: _ClassVar[int]
    template_id: str
    personalizations: _containers.RepeatedCompositeFieldContainer[Personalization]
    include_tracking: bool
    def __init__(self, template_id: _Optional[str] = ..., personalizations: _Optional[_Iterable[_Union[Personalization, _Mapping]]] = ..., include_tracking: bool = ..., **kwargs) -> None: ...
