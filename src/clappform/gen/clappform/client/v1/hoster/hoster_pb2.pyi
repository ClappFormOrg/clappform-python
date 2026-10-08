from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PredictionContext(_message.Message):
    __slots__ = ("model_name", "model_version", "data", "lime", "shap", "explain_type", "metadata")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    LIME_FIELD_NUMBER: _ClassVar[int]
    SHAP_FIELD_NUMBER: _ClassVar[int]
    EXPLAIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    model_version: str
    data: bytes
    lime: bytes
    shap: bytes
    explain_type: str
    metadata: bytes
    def __init__(self, model_name: _Optional[str] = ..., model_version: _Optional[str] = ..., data: _Optional[bytes] = ..., lime: _Optional[bytes] = ..., shap: _Optional[bytes] = ..., explain_type: _Optional[str] = ..., metadata: _Optional[bytes] = ...) -> None: ...
