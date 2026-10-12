from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from clappform.gen.clappform.client.v1.fileshare import fileshare_pb2 as _fileshare_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EmailRequest(_message.Message):
    __slots__ = ("template", "output_file", "data")
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FILE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    template: str
    output_file: str
    data: bytes
    def __init__(self, template: _Optional[str] = ..., output_file: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class FileRequest(_message.Message):
    __slots__ = ("file_name",)
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    def __init__(self, file_name: _Optional[str] = ...) -> None: ...
