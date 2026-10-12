from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SupportedShares(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED: _ClassVar[SupportedShares]
    PRIVATE: _ClassVar[SupportedShares]
    SFTP: _ClassVar[SupportedShares]
UNSPECIFIED: SupportedShares
PRIVATE: SupportedShares
SFTP: SupportedShares

class FileRequest(_message.Message):
    __slots__ = ("share", "file_path", "file_name", "chunk_size")
    SHARE_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    CHUNK_SIZE_FIELD_NUMBER: _ClassVar[int]
    share: SupportedShares
    file_path: str
    file_name: str
    chunk_size: int
    def __init__(self, share: _Optional[_Union[SupportedShares, str]] = ..., file_path: _Optional[str] = ..., file_name: _Optional[str] = ..., chunk_size: _Optional[int] = ...) -> None: ...

class FileData(_message.Message):
    __slots__ = ("file_name", "file_path", "file_data", "signed_url")
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    file_path: str
    file_data: bytes
    signed_url: str
    def __init__(self, file_name: _Optional[str] = ..., file_path: _Optional[str] = ..., file_data: _Optional[bytes] = ..., signed_url: _Optional[str] = ...) -> None: ...

class GenerateSASTokenRequest(_message.Message):
    __slots__ = ("share",)
    SHARE_FIELD_NUMBER: _ClassVar[int]
    share: SupportedShares
    def __init__(self, share: _Optional[_Union[SupportedShares, str]] = ...) -> None: ...

class GenerateSASTokenResponse(_message.Message):
    __slots__ = ("sas_url", "expiry_time", "can_read", "can_write", "can_delete", "can_list")
    SAS_URL_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_TIME_FIELD_NUMBER: _ClassVar[int]
    CAN_READ_FIELD_NUMBER: _ClassVar[int]
    CAN_WRITE_FIELD_NUMBER: _ClassVar[int]
    CAN_DELETE_FIELD_NUMBER: _ClassVar[int]
    CAN_LIST_FIELD_NUMBER: _ClassVar[int]
    sas_url: str
    expiry_time: int
    can_read: bool
    can_write: bool
    can_delete: bool
    can_list: bool
    def __init__(self, sas_url: _Optional[str] = ..., expiry_time: _Optional[int] = ..., can_read: bool = ..., can_write: bool = ..., can_delete: bool = ..., can_list: bool = ...) -> None: ...
