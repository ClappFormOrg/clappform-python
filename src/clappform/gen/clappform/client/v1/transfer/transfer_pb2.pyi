from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ExportRequest(_message.Message):
    __slots__ = ("id", "type", "name", "include_app", "include_queries", "include_actionflows", "include_questionnaires", "definition_id", "run_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_APP_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_QUERIES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ACTIONFLOWS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_QUESTIONNAIRES_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    name: str
    include_app: bool
    include_queries: bool
    include_actionflows: bool
    include_questionnaires: bool
    definition_id: str
    run_id: str
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., name: _Optional[str] = ..., include_app: bool = ..., include_queries: bool = ..., include_actionflows: bool = ..., include_questionnaires: bool = ..., definition_id: _Optional[str] = ..., run_id: _Optional[str] = ...) -> None: ...

class ActionflowExport(_message.Message):
    __slots__ = ("actionflow",)
    ACTIONFLOW_FIELD_NUMBER: _ClassVar[int]
    actionflow: bytes
    def __init__(self, actionflow: _Optional[bytes] = ...) -> None: ...

class ActionflowImport(_message.Message):
    __slots__ = ("actionflow",)
    ACTIONFLOW_FIELD_NUMBER: _ClassVar[int]
    actionflow: bytes
    def __init__(self, actionflow: _Optional[bytes] = ...) -> None: ...

class AppExport(_message.Message):
    __slots__ = ("app", "queries", "actionflows", "questionnaires")
    APP_FIELD_NUMBER: _ClassVar[int]
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    ACTIONFLOWS_FIELD_NUMBER: _ClassVar[int]
    QUESTIONNAIRES_FIELD_NUMBER: _ClassVar[int]
    app: bytes
    queries: bytes
    actionflows: bytes
    questionnaires: bytes
    def __init__(self, app: _Optional[bytes] = ..., queries: _Optional[bytes] = ..., actionflows: _Optional[bytes] = ..., questionnaires: _Optional[bytes] = ...) -> None: ...

class AppImport(_message.Message):
    __slots__ = ("app", "queries", "actionflows", "questionnaires", "overwrite", "definition_id", "run_id")
    APP_FIELD_NUMBER: _ClassVar[int]
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    ACTIONFLOWS_FIELD_NUMBER: _ClassVar[int]
    QUESTIONNAIRES_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    app: bytes
    queries: bytes
    actionflows: bytes
    questionnaires: bytes
    overwrite: bool
    definition_id: str
    run_id: str
    def __init__(self, app: _Optional[bytes] = ..., queries: _Optional[bytes] = ..., actionflows: _Optional[bytes] = ..., questionnaires: _Optional[bytes] = ..., overwrite: bool = ..., definition_id: _Optional[str] = ..., run_id: _Optional[str] = ...) -> None: ...
