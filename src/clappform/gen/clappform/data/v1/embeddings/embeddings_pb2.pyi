from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EmbeddingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMBEDDING_STATUS_UNKNOWN: _ClassVar[EmbeddingStatus]
    EMBEDDING_STATUS_PROCESSING: _ClassVar[EmbeddingStatus]
    EMBEDDING_STATUS_READY: _ClassVar[EmbeddingStatus]
    EMBEDDING_STATUS_FAILED: _ClassVar[EmbeddingStatus]
    EMBEDDING_STATUS_DELETED: _ClassVar[EmbeddingStatus]

class EmbeddingVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EMBEDDING_VISIBILITY_UNKNOWN: _ClassVar[EmbeddingVisibility]
    EMBEDDING_VISIBILITY_PRIVATE: _ClassVar[EmbeddingVisibility]
    EMBEDDING_VISIBILITY_TEAM: _ClassVar[EmbeddingVisibility]
EMBEDDING_STATUS_UNKNOWN: EmbeddingStatus
EMBEDDING_STATUS_PROCESSING: EmbeddingStatus
EMBEDDING_STATUS_READY: EmbeddingStatus
EMBEDDING_STATUS_FAILED: EmbeddingStatus
EMBEDDING_STATUS_DELETED: EmbeddingStatus
EMBEDDING_VISIBILITY_UNKNOWN: EmbeddingVisibility
EMBEDDING_VISIBILITY_PRIVATE: EmbeddingVisibility
EMBEDDING_VISIBILITY_TEAM: EmbeddingVisibility

class EmbeddingMetadata(_message.Message):
    __slots__ = ("id", "app_id", "user_id", "name", "filename", "mime_type", "size_bytes", "sha256", "metadata_collection", "vector_collection", "vector_index", "chunk_count", "embedding_model", "embedding_dim", "status", "status_message", "current_version", "tags", "created_at", "updated_at", "metadata_collection_slug", "vector_collection_slug", "visibility", "deleted_by", "summary", "topics", "summary_status")
    ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    VECTOR_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    VECTOR_INDEX_FIELD_NUMBER: _ClassVar[int]
    CHUNK_COUNT_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_MODEL_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_DIM_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_SLUG_FIELD_NUMBER: _ClassVar[int]
    VECTOR_COLLECTION_SLUG_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    DELETED_BY_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    app_id: str
    user_id: str
    name: str
    filename: str
    mime_type: str
    size_bytes: int
    sha256: str
    metadata_collection: str
    vector_collection: str
    vector_index: str
    chunk_count: int
    embedding_model: str
    embedding_dim: int
    status: EmbeddingStatus
    status_message: str
    current_version: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    created_at: int
    updated_at: int
    metadata_collection_slug: str
    vector_collection_slug: str
    visibility: EmbeddingVisibility
    deleted_by: str
    summary: str
    topics: _containers.RepeatedScalarFieldContainer[str]
    summary_status: str
    def __init__(self, id: _Optional[str] = ..., app_id: _Optional[str] = ..., user_id: _Optional[str] = ..., name: _Optional[str] = ..., filename: _Optional[str] = ..., mime_type: _Optional[str] = ..., size_bytes: _Optional[int] = ..., sha256: _Optional[str] = ..., metadata_collection: _Optional[str] = ..., vector_collection: _Optional[str] = ..., vector_index: _Optional[str] = ..., chunk_count: _Optional[int] = ..., embedding_model: _Optional[str] = ..., embedding_dim: _Optional[int] = ..., status: _Optional[_Union[EmbeddingStatus, str]] = ..., status_message: _Optional[str] = ..., current_version: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., metadata_collection_slug: _Optional[str] = ..., vector_collection_slug: _Optional[str] = ..., visibility: _Optional[_Union[EmbeddingVisibility, str]] = ..., deleted_by: _Optional[str] = ..., summary: _Optional[str] = ..., topics: _Optional[_Iterable[str]] = ..., summary_status: _Optional[str] = ...) -> None: ...

class EmbeddingFile(_message.Message):
    __slots__ = ("id", "name", "filename", "mime_type", "size_bytes", "metadata_collection", "metadata_collection_slug", "user_id", "visibility", "status", "deleted_by", "created_at", "updated_at", "tags")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_SLUG_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DELETED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    filename: str
    mime_type: str
    size_bytes: int
    metadata_collection: str
    metadata_collection_slug: str
    user_id: str
    visibility: EmbeddingVisibility
    status: EmbeddingStatus
    deleted_by: str
    created_at: int
    updated_at: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., filename: _Optional[str] = ..., mime_type: _Optional[str] = ..., size_bytes: _Optional[int] = ..., metadata_collection: _Optional[str] = ..., metadata_collection_slug: _Optional[str] = ..., user_id: _Optional[str] = ..., visibility: _Optional[_Union[EmbeddingVisibility, str]] = ..., status: _Optional[_Union[EmbeddingStatus, str]] = ..., deleted_by: _Optional[str] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class ListFilesRequest(_message.Message):
    __slots__ = ("app_id", "metadata_collection", "tags", "visibility", "cursor", "limit")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    metadata_collection: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    visibility: EmbeddingVisibility
    cursor: int
    limit: int
    def __init__(self, app_id: _Optional[str] = ..., metadata_collection: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., visibility: _Optional[_Union[EmbeddingVisibility, str]] = ..., cursor: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class ListTrashRequest(_message.Message):
    __slots__ = ("app_id", "metadata_collection", "cursor", "limit")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    metadata_collection: str
    cursor: int
    limit: int
    def __init__(self, app_id: _Optional[str] = ..., metadata_collection: _Optional[str] = ..., cursor: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class ListFilesResponse(_message.Message):
    __slots__ = ("files", "cursor")
    FILES_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[EmbeddingFile]
    cursor: int
    def __init__(self, files: _Optional[_Iterable[_Union[EmbeddingFile, _Mapping]]] = ..., cursor: _Optional[int] = ...) -> None: ...

class GetEmbeddingRequest(_message.Message):
    __slots__ = ("app_id", "id", "metadata_collection")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    id: str
    metadata_collection: str
    def __init__(self, app_id: _Optional[str] = ..., id: _Optional[str] = ..., metadata_collection: _Optional[str] = ...) -> None: ...

class DeleteEmbeddingRequest(_message.Message):
    __slots__ = ("app_id", "id", "metadata_collection")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    id: str
    metadata_collection: str
    def __init__(self, app_id: _Optional[str] = ..., id: _Optional[str] = ..., metadata_collection: _Optional[str] = ...) -> None: ...

class ReembedRequest(_message.Message):
    __slots__ = ("app_id", "vector_collection", "target_model", "dry_run")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    VECTOR_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    TARGET_MODEL_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    vector_collection: str
    target_model: str
    dry_run: bool
    def __init__(self, app_id: _Optional[str] = ..., vector_collection: _Optional[str] = ..., target_model: _Optional[str] = ..., dry_run: bool = ...) -> None: ...

class CleanupOrphansRequest(_message.Message):
    __slots__ = ("app_id", "metadata_collection", "older_than_ms")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    OLDER_THAN_MS_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    metadata_collection: str
    older_than_ms: int
    def __init__(self, app_id: _Optional[str] = ..., metadata_collection: _Optional[str] = ..., older_than_ms: _Optional[int] = ...) -> None: ...

class CleanupOrphansResponse(_message.Message):
    __slots__ = ("swept_count", "finalized_count", "failed_count")
    SWEPT_COUNT_FIELD_NUMBER: _ClassVar[int]
    FINALIZED_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAILED_COUNT_FIELD_NUMBER: _ClassVar[int]
    swept_count: int
    finalized_count: int
    failed_count: int
    def __init__(self, swept_count: _Optional[int] = ..., finalized_count: _Optional[int] = ..., failed_count: _Optional[int] = ...) -> None: ...

class ReembedResponse(_message.Message):
    __slots__ = ("affected_record_count", "dry_run")
    AFFECTED_RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    affected_record_count: int
    dry_run: bool
    def __init__(self, affected_record_count: _Optional[int] = ..., dry_run: bool = ...) -> None: ...

class ListSupportedFileTypesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSupportedFileTypesResponse(_message.Message):
    __slots__ = ("mime_types", "descriptions")
    MIME_TYPES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    mime_types: _containers.RepeatedScalarFieldContainer[str]
    descriptions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, mime_types: _Optional[_Iterable[str]] = ..., descriptions: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateEmbeddingRequest(_message.Message):
    __slots__ = ("app_id", "metadata_collection", "vector_collection", "filename", "name", "size_bytes", "tags", "visibility")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    VECTOR_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    metadata_collection: str
    vector_collection: str
    filename: str
    name: str
    size_bytes: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    visibility: EmbeddingVisibility
    def __init__(self, app_id: _Optional[str] = ..., metadata_collection: _Optional[str] = ..., vector_collection: _Optional[str] = ..., filename: _Optional[str] = ..., name: _Optional[str] = ..., size_bytes: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ..., visibility: _Optional[_Union[EmbeddingVisibility, str]] = ...) -> None: ...

class CreateEmbeddingResponse(_message.Message):
    __slots__ = ("metadata", "upload_url", "upload_expires_at", "dedup_hit")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    DEDUP_HIT_FIELD_NUMBER: _ClassVar[int]
    metadata: EmbeddingMetadata
    upload_url: str
    upload_expires_at: int
    dedup_hit: bool
    def __init__(self, metadata: _Optional[_Union[EmbeddingMetadata, _Mapping]] = ..., upload_url: _Optional[str] = ..., upload_expires_at: _Optional[int] = ..., dedup_hit: bool = ...) -> None: ...

class FinalizeEmbeddingRequest(_message.Message):
    __slots__ = ("app_id", "id", "metadata_collection")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    id: str
    metadata_collection: str
    def __init__(self, app_id: _Optional[str] = ..., id: _Optional[str] = ..., metadata_collection: _Optional[str] = ...) -> None: ...
