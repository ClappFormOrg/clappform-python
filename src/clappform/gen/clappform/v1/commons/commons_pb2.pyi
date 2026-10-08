from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Message(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class Read(_message.Message):
    __slots__ = ("id", "detail_level", "include_deleted")
    ID_FIELD_NUMBER: _ClassVar[int]
    DETAIL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: _ClassVar[int]
    id: str
    detail_level: int
    include_deleted: bool
    def __init__(self, id: _Optional[str] = ..., detail_level: _Optional[int] = ..., include_deleted: bool = ...) -> None: ...

class PaginationRequest(_message.Message):
    __slots__ = ("page", "limit", "batch_size", "query_parameters", "include_deleted", "detail_level", "sort")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
    QUERY_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: _ClassVar[int]
    DETAIL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    page: int
    limit: int
    batch_size: int
    query_parameters: str
    include_deleted: bool
    detail_level: int
    sort: str
    def __init__(self, page: _Optional[int] = ..., limit: _Optional[int] = ..., batch_size: _Optional[int] = ..., query_parameters: _Optional[str] = ..., include_deleted: bool = ..., detail_level: _Optional[int] = ..., sort: _Optional[str] = ...) -> None: ...

class Pagination(_message.Message):
    __slots__ = ("page", "limit", "total", "pages")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    PAGES_FIELD_NUMBER: _ClassVar[int]
    page: int
    limit: int
    total: int
    pages: int
    def __init__(self, page: _Optional[int] = ..., limit: _Optional[int] = ..., total: _Optional[int] = ..., pages: _Optional[int] = ...) -> None: ...
