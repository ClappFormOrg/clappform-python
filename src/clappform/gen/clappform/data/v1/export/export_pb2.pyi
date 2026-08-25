from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExportFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXPORT_FORMAT_UNSPECIFIED: _ClassVar[ExportFormat]
    EXPORT_FORMAT_CSV: _ClassVar[ExportFormat]
    EXPORT_FORMAT_XLSX: _ClassVar[ExportFormat]
    EXPORT_FORMAT_JSON: _ClassVar[ExportFormat]
    EXPORT_FORMAT_BSON: _ClassVar[ExportFormat]

class ExportStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXPORT_STATUS_UNSPECIFIED: _ClassVar[ExportStatus]
    EXPORT_STATUS_QUEUED: _ClassVar[ExportStatus]
    EXPORT_STATUS_RUNNING: _ClassVar[ExportStatus]
    EXPORT_STATUS_READY: _ClassVar[ExportStatus]
    EXPORT_STATUS_FAILED: _ClassVar[ExportStatus]
    EXPORT_STATUS_CANCELLED: _ClassVar[ExportStatus]
EXPORT_FORMAT_UNSPECIFIED: ExportFormat
EXPORT_FORMAT_CSV: ExportFormat
EXPORT_FORMAT_XLSX: ExportFormat
EXPORT_FORMAT_JSON: ExportFormat
EXPORT_FORMAT_BSON: ExportFormat
EXPORT_STATUS_UNSPECIFIED: ExportStatus
EXPORT_STATUS_QUEUED: ExportStatus
EXPORT_STATUS_RUNNING: ExportStatus
EXPORT_STATUS_READY: ExportStatus
EXPORT_STATUS_FAILED: ExportStatus
EXPORT_STATUS_CANCELLED: ExportStatus

class PipelineSource(_message.Message):
    __slots__ = ("collection", "pipeline")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    collection: str
    pipeline: bytes
    def __init__(self, collection: _Optional[str] = ..., pipeline: _Optional[bytes] = ...) -> None: ...

class SavedQuerySource(_message.Message):
    __slots__ = ("query_id",)
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    def __init__(self, query_id: _Optional[str] = ...) -> None: ...

class CreateExportRequest(_message.Message):
    __slots__ = ("inline", "saved_query", "format", "filename", "notify_on_complete", "disable_compression")
    INLINE_FIELD_NUMBER: _ClassVar[int]
    SAVED_QUERY_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    NOTIFY_ON_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    DISABLE_COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    inline: PipelineSource
    saved_query: SavedQuerySource
    format: ExportFormat
    filename: str
    notify_on_complete: bool
    disable_compression: bool
    def __init__(self, inline: _Optional[_Union[PipelineSource, _Mapping]] = ..., saved_query: _Optional[_Union[SavedQuerySource, _Mapping]] = ..., format: _Optional[_Union[ExportFormat, str]] = ..., filename: _Optional[str] = ..., notify_on_complete: bool = ..., disable_compression: bool = ...) -> None: ...

class GetExportRequest(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class CancelExportRequest(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class ListExportsRequest(_message.Message):
    __slots__ = ("status", "limit")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    status: ExportStatus
    limit: int
    def __init__(self, status: _Optional[_Union[ExportStatus, str]] = ..., limit: _Optional[int] = ...) -> None: ...

class ListExportsResponse(_message.Message):
    __slots__ = ("exports",)
    EXPORTS_FIELD_NUMBER: _ClassVar[int]
    exports: _containers.RepeatedCompositeFieldContainer[Export]
    def __init__(self, exports: _Optional[_Iterable[_Union[Export, _Mapping]]] = ...) -> None: ...

class Export(_message.Message):
    __slots__ = ("job_id", "status", "format", "filename", "sas_url", "sas_expires_at", "rows_written", "rows_skipped", "bytes_written", "failure_reason", "created_at", "started_at", "completed_at", "disable_compression")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    SAS_URL_FIELD_NUMBER: _ClassVar[int]
    SAS_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    ROWS_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    ROWS_SKIPPED_FIELD_NUMBER: _ClassVar[int]
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    FAILURE_REASON_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    DISABLE_COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    status: ExportStatus
    format: ExportFormat
    filename: str
    sas_url: str
    sas_expires_at: int
    rows_written: int
    rows_skipped: int
    bytes_written: int
    failure_reason: str
    created_at: int
    started_at: int
    completed_at: int
    disable_compression: bool
    def __init__(self, job_id: _Optional[str] = ..., status: _Optional[_Union[ExportStatus, str]] = ..., format: _Optional[_Union[ExportFormat, str]] = ..., filename: _Optional[str] = ..., sas_url: _Optional[str] = ..., sas_expires_at: _Optional[int] = ..., rows_written: _Optional[int] = ..., rows_skipped: _Optional[int] = ..., bytes_written: _Optional[int] = ..., failure_reason: _Optional[str] = ..., created_at: _Optional[int] = ..., started_at: _Optional[int] = ..., completed_at: _Optional[int] = ..., disable_compression: bool = ...) -> None: ...
