from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from clappform.gen.clappform.v1.commons import commons_pb2 as _commons_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Capability(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CAPABILITY_UNSPECIFIED: _ClassVar[Capability]
    CAPABILITY_CHAT: _ClassVar[Capability]
    CAPABILITY_EMBEDDING: _ClassVar[Capability]
    CAPABILITY_SUMMARISATION: _ClassVar[Capability]
    CAPABILITY_INTENT: _ClassVar[Capability]
    CAPABILITY_QUERY_PLAN: _ClassVar[Capability]
    CAPABILITY_QUERY_ANALYSIS: _ClassVar[Capability]
    CAPABILITY_AUTONAME: _ClassVar[Capability]
    CAPABILITY_FKMETADATA: _ClassVar[Capability]
CAPABILITY_UNSPECIFIED: Capability
CAPABILITY_CHAT: Capability
CAPABILITY_EMBEDDING: Capability
CAPABILITY_SUMMARISATION: Capability
CAPABILITY_INTENT: Capability
CAPABILITY_QUERY_PLAN: Capability
CAPABILITY_QUERY_ANALYSIS: Capability
CAPABILITY_AUTONAME: Capability
CAPABILITY_FKMETADATA: Capability

class CapabilityDefault(_message.Message):
    __slots__ = ("capability", "model_id", "updated_at", "updated_by")
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_BY_FIELD_NUMBER: _ClassVar[int]
    capability: Capability
    model_id: str
    updated_at: int
    updated_by: str
    def __init__(self, capability: _Optional[_Union[Capability, str]] = ..., model_id: _Optional[str] = ..., updated_at: _Optional[int] = ..., updated_by: _Optional[str] = ...) -> None: ...

class SetCapabilityDefaultRequest(_message.Message):
    __slots__ = ("capability", "model_id")
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    capability: Capability
    model_id: str
    def __init__(self, capability: _Optional[_Union[Capability, str]] = ..., model_id: _Optional[str] = ...) -> None: ...

class SetCapabilityDefaultResponse(_message.Message):
    __slots__ = ("default",)
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    default: CapabilityDefault
    def __init__(self, default: _Optional[_Union[CapabilityDefault, _Mapping]] = ...) -> None: ...

class GetCapabilityDefaultsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCapabilityDefaultsResponse(_message.Message):
    __slots__ = ("defaults",)
    DEFAULTS_FIELD_NUMBER: _ClassVar[int]
    defaults: _containers.RepeatedCompositeFieldContainer[CapabilityDefault]
    def __init__(self, defaults: _Optional[_Iterable[_Union[CapabilityDefault, _Mapping]]] = ...) -> None: ...

class ClearCapabilityDefaultRequest(_message.Message):
    __slots__ = ("capability",)
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    capability: Capability
    def __init__(self, capability: _Optional[_Union[Capability, str]] = ...) -> None: ...

class ClearCapabilityDefaultResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Model(_message.Message):
    __slots__ = ("id", "name", "provider", "supports_images", "supports_tools", "supports_json_mode", "max_context_tokens")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_IMAGES_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TOOLS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_JSON_MODE_FIELD_NUMBER: _ClassVar[int]
    MAX_CONTEXT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    provider: str
    supports_images: bool
    supports_tools: bool
    supports_json_mode: bool
    max_context_tokens: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., provider: _Optional[str] = ..., supports_images: bool = ..., supports_tools: bool = ..., supports_json_mode: bool = ..., max_context_tokens: _Optional[int] = ...) -> None: ...

class Models(_message.Message):
    __slots__ = ("models",)
    MODELS_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[Model]
    def __init__(self, models: _Optional[_Iterable[_Union[Model, _Mapping]]] = ...) -> None: ...

class GetModelsRequest(_message.Message):
    __slots__ = ("capabilities", "include_all")
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ALL_FIELD_NUMBER: _ClassVar[int]
    capabilities: _containers.RepeatedScalarFieldContainer[Capability]
    include_all: bool
    def __init__(self, capabilities: _Optional[_Iterable[_Union[Capability, str]]] = ..., include_all: bool = ...) -> None: ...

class ModelDescriptorAdmin(_message.Message):
    __slots__ = ("id", "name", "provider", "chat_url", "model", "api_key", "temperature", "max_tokens", "max_context_tokens", "supports_images", "supports_tools", "supports_json_mode", "native_system", "price_per_input_token", "price_per_output_token", "fallback_model_id", "enabled", "allow_data_access", "reasoning_series", "capabilities", "timeout_seconds")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CHAT_URL_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    MAX_CONTEXT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_IMAGES_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_TOOLS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_JSON_MODE_FIELD_NUMBER: _ClassVar[int]
    NATIVE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    PRICE_PER_INPUT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PRICE_PER_OUTPUT_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ALLOW_DATA_ACCESS_FIELD_NUMBER: _ClassVar[int]
    REASONING_SERIES_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    provider: str
    chat_url: str
    model: str
    api_key: str
    temperature: float
    max_tokens: int
    max_context_tokens: int
    supports_images: bool
    supports_tools: bool
    supports_json_mode: bool
    native_system: bool
    price_per_input_token: float
    price_per_output_token: float
    fallback_model_id: str
    enabled: bool
    allow_data_access: bool
    reasoning_series: bool
    capabilities: _containers.RepeatedScalarFieldContainer[Capability]
    timeout_seconds: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., provider: _Optional[str] = ..., chat_url: _Optional[str] = ..., model: _Optional[str] = ..., api_key: _Optional[str] = ..., temperature: _Optional[float] = ..., max_tokens: _Optional[int] = ..., max_context_tokens: _Optional[int] = ..., supports_images: bool = ..., supports_tools: bool = ..., supports_json_mode: bool = ..., native_system: bool = ..., price_per_input_token: _Optional[float] = ..., price_per_output_token: _Optional[float] = ..., fallback_model_id: _Optional[str] = ..., enabled: bool = ..., allow_data_access: bool = ..., reasoning_series: bool = ..., capabilities: _Optional[_Iterable[_Union[Capability, str]]] = ..., timeout_seconds: _Optional[int] = ...) -> None: ...

class CreateModelRequest(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: ModelDescriptorAdmin
    def __init__(self, model: _Optional[_Union[ModelDescriptorAdmin, _Mapping]] = ...) -> None: ...

class CreateModelResponse(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: ModelDescriptorAdmin
    def __init__(self, model: _Optional[_Union[ModelDescriptorAdmin, _Mapping]] = ...) -> None: ...

class UpdateModelRequest(_message.Message):
    __slots__ = ("id", "model")
    ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    model: ModelDescriptorAdmin
    def __init__(self, id: _Optional[str] = ..., model: _Optional[_Union[ModelDescriptorAdmin, _Mapping]] = ...) -> None: ...

class UpdateModelResponse(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: ModelDescriptorAdmin
    def __init__(self, model: _Optional[_Union[ModelDescriptorAdmin, _Mapping]] = ...) -> None: ...

class DeleteModelRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class SetModelEnabledRequest(_message.Message):
    __slots__ = ("id", "enabled")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    id: str
    enabled: bool
    def __init__(self, id: _Optional[str] = ..., enabled: bool = ...) -> None: ...

class SetModelEnabledResponse(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: ModelDescriptorAdmin
    def __init__(self, model: _Optional[_Union[ModelDescriptorAdmin, _Mapping]] = ...) -> None: ...

class GetModelAdminRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetModelAdminResponse(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: ModelDescriptorAdmin
    def __init__(self, model: _Optional[_Union[ModelDescriptorAdmin, _Mapping]] = ...) -> None: ...

class RewriteModelRequest(_message.Message):
    __slots__ = ("app_id", "from_model_id", "to_model_id", "dry_run")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    TO_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    from_model_id: str
    to_model_id: str
    dry_run: bool
    def __init__(self, app_id: _Optional[str] = ..., from_model_id: _Optional[str] = ..., to_model_id: _Optional[str] = ..., dry_run: bool = ...) -> None: ...

class RewriteModelResponse(_message.Message):
    __slots__ = ("affected_chat_count", "dry_run")
    AFFECTED_CHAT_COUNT_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    affected_chat_count: int
    dry_run: bool
    def __init__(self, affected_chat_count: _Optional[int] = ..., dry_run: bool = ...) -> None: ...
