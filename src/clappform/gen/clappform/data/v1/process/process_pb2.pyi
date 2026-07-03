from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetLandingPageRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetConformanceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListProcessesRequest(_message.Message):
    __slots__ = ("limit", "offset")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    limit: int
    offset: int
    def __init__(self, limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class DescribeProcessRequest(_message.Message):
    __slots__ = ("process_id",)
    PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    process_id: str
    def __init__(self, process_id: _Optional[str] = ...) -> None: ...

class ExecuteRequest(_message.Message):
    __slots__ = ("process_id", "inputs", "response_mode")
    PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_MODE_FIELD_NUMBER: _ClassVar[int]
    process_id: str
    inputs: _struct_pb2.Struct
    response_mode: str
    def __init__(self, process_id: _Optional[str] = ..., inputs: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., response_mode: _Optional[str] = ...) -> None: ...

class GetJobRequest(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class DismissJobRequest(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class ConformanceDeclaration(_message.Message):
    __slots__ = ("conforms_to",)
    CONFORMS_TO_FIELD_NUMBER: _ClassVar[int]
    conforms_to: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, conforms_to: _Optional[_Iterable[str]] = ...) -> None: ...

class ProcessList(_message.Message):
    __slots__ = ("processes", "total_count", "links")
    PROCESSES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    processes: _containers.RepeatedCompositeFieldContainer[ProcessSummary]
    total_count: int
    links: _containers.RepeatedCompositeFieldContainer[Link]
    def __init__(self, processes: _Optional[_Iterable[_Union[ProcessSummary, _Mapping]]] = ..., total_count: _Optional[int] = ..., links: _Optional[_Iterable[_Union[Link, _Mapping]]] = ...) -> None: ...

class ProcessSummary(_message.Message):
    __slots__ = ("id", "title", "description", "version", "job_control_options", "output_transmission", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    JOB_CONTROL_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_TRANSMISSION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    version: str
    job_control_options: _containers.RepeatedScalarFieldContainer[str]
    output_transmission: _containers.RepeatedScalarFieldContainer[str]
    metadata: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., version: _Optional[str] = ..., job_control_options: _Optional[_Iterable[str]] = ..., output_transmission: _Optional[_Iterable[str]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ProcessDescription(_message.Message):
    __slots__ = ("id", "title", "description", "version", "job_control_options", "output_transmission", "inputs", "outputs", "metadata", "links")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    JOB_CONTROL_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_TRANSMISSION_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    version: str
    job_control_options: _containers.RepeatedScalarFieldContainer[str]
    output_transmission: _containers.RepeatedScalarFieldContainer[str]
    inputs: _containers.RepeatedCompositeFieldContainer[InputDescription]
    outputs: _containers.RepeatedCompositeFieldContainer[OutputDescription]
    metadata: _struct_pb2.Struct
    links: _containers.RepeatedCompositeFieldContainer[Link]
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., version: _Optional[str] = ..., job_control_options: _Optional[_Iterable[str]] = ..., output_transmission: _Optional[_Iterable[str]] = ..., inputs: _Optional[_Iterable[_Union[InputDescription, _Mapping]]] = ..., outputs: _Optional[_Iterable[_Union[OutputDescription, _Mapping]]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., links: _Optional[_Iterable[_Union[Link, _Mapping]]] = ...) -> None: ...

class InputDescription(_message.Message):
    __slots__ = ("id", "title", "description", "schema", "min_occurs", "max_occurs")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    MIN_OCCURS_FIELD_NUMBER: _ClassVar[int]
    MAX_OCCURS_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    schema: _struct_pb2.Struct
    min_occurs: int
    max_occurs: int
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., schema: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., min_occurs: _Optional[int] = ..., max_occurs: _Optional[int] = ...) -> None: ...

class OutputDescription(_message.Message):
    __slots__ = ("id", "title", "description", "schema")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    schema: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., schema: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ExecuteResponse(_message.Message):
    __slots__ = ("job", "outputs")
    JOB_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    job: JobStatus
    outputs: _struct_pb2.Struct
    def __init__(self, job: _Optional[_Union[JobStatus, _Mapping]] = ..., outputs: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class JobStatus(_message.Message):
    __slots__ = ("job_id", "status", "message", "progress", "created", "started", "finished", "updated", "links")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    STARTED_FIELD_NUMBER: _ClassVar[int]
    FINISHED_FIELD_NUMBER: _ClassVar[int]
    UPDATED_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    status: str
    message: str
    progress: int
    created: int
    started: int
    finished: int
    updated: int
    links: _containers.RepeatedCompositeFieldContainer[Link]
    def __init__(self, job_id: _Optional[str] = ..., status: _Optional[str] = ..., message: _Optional[str] = ..., progress: _Optional[int] = ..., created: _Optional[int] = ..., started: _Optional[int] = ..., finished: _Optional[int] = ..., updated: _Optional[int] = ..., links: _Optional[_Iterable[_Union[Link, _Mapping]]] = ...) -> None: ...

class JobResults(_message.Message):
    __slots__ = ("job_id", "outputs", "links")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    outputs: _struct_pb2.Struct
    links: _containers.RepeatedCompositeFieldContainer[Link]
    def __init__(self, job_id: _Optional[str] = ..., outputs: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., links: _Optional[_Iterable[_Union[Link, _Mapping]]] = ...) -> None: ...

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
