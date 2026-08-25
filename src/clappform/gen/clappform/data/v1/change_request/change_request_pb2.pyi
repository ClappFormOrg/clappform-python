from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChangeRequest(_message.Message):
    __slots__ = ("data", "collection")
    DATA_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    collection: str
    def __init__(self, data: _Optional[bytes] = ..., collection: _Optional[str] = ...) -> None: ...

class RequestChangeResponse(_message.Message):
    __slots__ = ("request_id",)
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    def __init__(self, request_id: _Optional[str] = ...) -> None: ...

class UpdateStatusRequest(_message.Message):
    __slots__ = ("request_id", "collection", "note")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    collection: str
    note: str
    def __init__(self, request_id: _Optional[str] = ..., collection: _Optional[str] = ..., note: _Optional[str] = ...) -> None: ...

class ModifyChangeRequest(_message.Message):
    __slots__ = ("request_id", "collection", "note", "data")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    collection: str
    note: str
    data: bytes
    def __init__(self, request_id: _Optional[str] = ..., collection: _Optional[str] = ..., note: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class ModifyApproverRequest(_message.Message):
    __slots__ = ("request_id", "collection", "note", "approver_id")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    APPROVER_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    collection: str
    note: str
    approver_id: str
    def __init__(self, request_id: _Optional[str] = ..., collection: _Optional[str] = ..., note: _Optional[str] = ..., approver_id: _Optional[str] = ...) -> None: ...

class CreateSuggestionRequest(_message.Message):
    __slots__ = ("collection", "target_doc_id", "field_name", "original_value", "suggestions", "source")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    TARGET_DOC_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    collection: str
    target_doc_id: str
    field_name: str
    original_value: bytes
    suggestions: _containers.RepeatedCompositeFieldContainer[SuggestionOption]
    source: str
    def __init__(self, collection: _Optional[str] = ..., target_doc_id: _Optional[str] = ..., field_name: _Optional[str] = ..., original_value: _Optional[bytes] = ..., suggestions: _Optional[_Iterable[_Union[SuggestionOption, _Mapping]]] = ..., source: _Optional[str] = ...) -> None: ...

class SuggestionOption(_message.Message):
    __slots__ = ("id", "suggested_value", "confidence", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    SUGGESTED_VALUE_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    suggested_value: bytes
    confidence: float
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., suggested_value: _Optional[bytes] = ..., confidence: _Optional[float] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class AcceptSuggestionRequest(_message.Message):
    __slots__ = ("collection", "request_id", "suggestion_id", "note", "update_dictionary")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SUGGESTION_ID_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DICTIONARY_FIELD_NUMBER: _ClassVar[int]
    collection: str
    request_id: str
    suggestion_id: str
    note: str
    update_dictionary: bool
    def __init__(self, collection: _Optional[str] = ..., request_id: _Optional[str] = ..., suggestion_id: _Optional[str] = ..., note: _Optional[str] = ..., update_dictionary: bool = ...) -> None: ...

class RejectSuggestionsRequest(_message.Message):
    __slots__ = ("collection", "request_id", "note")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    collection: str
    request_id: str
    note: str
    def __init__(self, collection: _Optional[str] = ..., request_id: _Optional[str] = ..., note: _Optional[str] = ...) -> None: ...

class AcceptWithCustomValueRequest(_message.Message):
    __slots__ = ("collection", "request_id", "custom_value", "note", "update_dictionary")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_VALUE_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DICTIONARY_FIELD_NUMBER: _ClassVar[int]
    collection: str
    request_id: str
    custom_value: bytes
    note: str
    update_dictionary: bool
    def __init__(self, collection: _Optional[str] = ..., request_id: _Optional[str] = ..., custom_value: _Optional[bytes] = ..., note: _Optional[str] = ..., update_dictionary: bool = ...) -> None: ...

class GetConflictsRequests(_message.Message):
    __slots__ = ("collection",)
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    collection: str
    def __init__(self, collection: _Optional[str] = ...) -> None: ...

class GetOneConflictsRequest(_message.Message):
    __slots__ = ("collection", "request_id")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    collection: str
    request_id: str
    def __init__(self, collection: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class ConflictingRequest(_message.Message):
    __slots__ = ("request_id", "conflicting_fields", "detected_at")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONFLICTING_FIELDS_FIELD_NUMBER: _ClassVar[int]
    DETECTED_AT_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    conflicting_fields: _containers.RepeatedScalarFieldContainer[str]
    detected_at: int
    def __init__(self, request_id: _Optional[str] = ..., conflicting_fields: _Optional[_Iterable[str]] = ..., detected_at: _Optional[int] = ...) -> None: ...

class SuggestionConflictGroup(_message.Message):
    __slots__ = ("field_name", "target_doc_id", "original_name", "original_uri", "original_unmapped_value", "request_ids", "merged_options", "detected_at", "last_checked_at")
    FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_DOC_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_NAME_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_URI_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_UNMAPPED_VALUE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_IDS_FIELD_NUMBER: _ClassVar[int]
    MERGED_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    DETECTED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_CHECKED_AT_FIELD_NUMBER: _ClassVar[int]
    field_name: str
    target_doc_id: str
    original_name: str
    original_uri: str
    original_unmapped_value: bytes
    request_ids: _containers.RepeatedScalarFieldContainer[str]
    merged_options: _containers.RepeatedCompositeFieldContainer[SuggestionOptionDetail]
    detected_at: int
    last_checked_at: int
    def __init__(self, field_name: _Optional[str] = ..., target_doc_id: _Optional[str] = ..., original_name: _Optional[str] = ..., original_uri: _Optional[str] = ..., original_unmapped_value: _Optional[bytes] = ..., request_ids: _Optional[_Iterable[str]] = ..., merged_options: _Optional[_Iterable[_Union[SuggestionOptionDetail, _Mapping]]] = ..., detected_at: _Optional[int] = ..., last_checked_at: _Optional[int] = ...) -> None: ...

class SuggestionOptionDetail(_message.Message):
    __slots__ = ("id", "suggested_value", "confidence", "metadata", "source_request_id")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    SUGGESTED_VALUE_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SOURCE_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    suggested_value: bytes
    confidence: float
    metadata: _containers.ScalarMap[str, str]
    source_request_id: str
    def __init__(self, id: _Optional[str] = ..., suggested_value: _Optional[bytes] = ..., confidence: _Optional[float] = ..., metadata: _Optional[_Mapping[str, str]] = ..., source_request_id: _Optional[str] = ...) -> None: ...

class ConflictsResponseAll(_message.Message):
    __slots__ = ("conflicts",)
    CONFLICTS_FIELD_NUMBER: _ClassVar[int]
    conflicts: _containers.RepeatedCompositeFieldContainer[ConflictsResponseOne]
    def __init__(self, conflicts: _Optional[_Iterable[_Union[ConflictsResponseOne, _Mapping]]] = ...) -> None: ...

class ConflictsResponseOne(_message.Message):
    __slots__ = ("request_id", "has_conflicts", "conflicting_requests", "detected_at", "last_checked_at", "conflict_group")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    HAS_CONFLICTS_FIELD_NUMBER: _ClassVar[int]
    CONFLICTING_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    DETECTED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_CHECKED_AT_FIELD_NUMBER: _ClassVar[int]
    CONFLICT_GROUP_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    has_conflicts: bool
    conflicting_requests: _containers.RepeatedCompositeFieldContainer[ConflictingRequest]
    detected_at: int
    last_checked_at: int
    conflict_group: SuggestionConflictGroup
    def __init__(self, request_id: _Optional[str] = ..., has_conflicts: bool = ..., conflicting_requests: _Optional[_Iterable[_Union[ConflictingRequest, _Mapping]]] = ..., detected_at: _Optional[int] = ..., last_checked_at: _Optional[int] = ..., conflict_group: _Optional[_Union[SuggestionConflictGroup, _Mapping]] = ...) -> None: ...
