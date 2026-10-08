from clappform.gen.google.api import annotations_pb2 as _annotations_pb2
from clappform.gen.grpc.gateway.protoc_gen_openapiv2.options import annotations_pb2 as _annotations_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PolicyConditionRequest(_message.Message):
    __slots__ = ("type", "previous_step_id", "condition_quorum")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_STEP_ID_FIELD_NUMBER: _ClassVar[int]
    CONDITION_QUORUM_FIELD_NUMBER: _ClassVar[int]
    type: str
    previous_step_id: str
    condition_quorum: str
    def __init__(self, type: _Optional[str] = ..., previous_step_id: _Optional[str] = ..., condition_quorum: _Optional[str] = ...) -> None: ...

class PolicyStepRequest(_message.Message):
    __slots__ = ("step_id", "channel", "delay_seconds", "conditions", "recipients_override")
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    DELAY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    step_id: str
    channel: str
    delay_seconds: int
    conditions: _containers.RepeatedCompositeFieldContainer[PolicyConditionRequest]
    recipients_override: str
    def __init__(self, step_id: _Optional[str] = ..., channel: _Optional[str] = ..., delay_seconds: _Optional[int] = ..., conditions: _Optional[_Iterable[_Union[PolicyConditionRequest, _Mapping]]] = ..., recipients_override: _Optional[str] = ...) -> None: ...

class CreatePolicyRequest(_message.Message):
    __slots__ = ("name", "description", "steps")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    steps: _containers.RepeatedCompositeFieldContainer[PolicyStepRequest]
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[PolicyStepRequest, _Mapping]]] = ...) -> None: ...

class UpdatePolicyRequest(_message.Message):
    __slots__ = ("id", "name", "description", "steps")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    steps: _containers.RepeatedCompositeFieldContainer[PolicyStepRequest]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[PolicyStepRequest, _Mapping]]] = ...) -> None: ...

class GetPolicyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeletePolicyRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ListPoliciesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PolicyConditionResponse(_message.Message):
    __slots__ = ("type", "previous_step_id", "condition_quorum")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_STEP_ID_FIELD_NUMBER: _ClassVar[int]
    CONDITION_QUORUM_FIELD_NUMBER: _ClassVar[int]
    type: str
    previous_step_id: str
    condition_quorum: str
    def __init__(self, type: _Optional[str] = ..., previous_step_id: _Optional[str] = ..., condition_quorum: _Optional[str] = ...) -> None: ...

class PolicyStepResponse(_message.Message):
    __slots__ = ("step_id", "channel", "delay_seconds", "conditions", "recipients_override")
    STEP_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    DELAY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    step_id: str
    channel: str
    delay_seconds: int
    conditions: _containers.RepeatedCompositeFieldContainer[PolicyConditionResponse]
    recipients_override: str
    def __init__(self, step_id: _Optional[str] = ..., channel: _Optional[str] = ..., delay_seconds: _Optional[int] = ..., conditions: _Optional[_Iterable[_Union[PolicyConditionResponse, _Mapping]]] = ..., recipients_override: _Optional[str] = ...) -> None: ...

class PolicyResponse(_message.Message):
    __slots__ = ("id", "location", "name", "description", "version", "steps", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    location: str
    name: str
    description: str
    version: int
    steps: _containers.RepeatedCompositeFieldContainer[PolicyStepResponse]
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., location: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., version: _Optional[int] = ..., steps: _Optional[_Iterable[_Union[PolicyStepResponse, _Mapping]]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class ListPoliciesResponse(_message.Message):
    __slots__ = ("policies",)
    POLICIES_FIELD_NUMBER: _ClassVar[int]
    policies: _containers.RepeatedCompositeFieldContainer[PolicyResponse]
    def __init__(self, policies: _Optional[_Iterable[_Union[PolicyResponse, _Mapping]]] = ...) -> None: ...

class DeletePolicyResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class FromPolicyRecipient(_message.Message):
    __slots__ = ("id", "email", "phone", "variables")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    phone: str
    variables: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., phone: _Optional[str] = ..., variables: _Optional[_Mapping[str, str]] = ...) -> None: ...

class FromPolicyRequest(_message.Message):
    __slots__ = ("policy_id", "subject", "body", "variables", "recipients", "escalation_contacts", "priority", "semantic_theme")
    class VariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class EscalationContactsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTS_FIELD_NUMBER: _ClassVar[int]
    ESCALATION_CONTACTS_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    SEMANTIC_THEME_FIELD_NUMBER: _ClassVar[int]
    policy_id: str
    subject: str
    body: str
    variables: _containers.ScalarMap[str, str]
    recipients: _containers.RepeatedCompositeFieldContainer[FromPolicyRecipient]
    escalation_contacts: _containers.ScalarMap[str, str]
    priority: str
    semantic_theme: str
    def __init__(self, policy_id: _Optional[str] = ..., subject: _Optional[str] = ..., body: _Optional[str] = ..., variables: _Optional[_Mapping[str, str]] = ..., recipients: _Optional[_Iterable[_Union[FromPolicyRecipient, _Mapping]]] = ..., escalation_contacts: _Optional[_Mapping[str, str]] = ..., priority: _Optional[str] = ..., semantic_theme: _Optional[str] = ...) -> None: ...

class FromPolicyResponse(_message.Message):
    __slots__ = ("batch_id", "policy_version_id")
    BATCH_ID_FIELD_NUMBER: _ClassVar[int]
    POLICY_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    batch_id: str
    policy_version_id: int
    def __init__(self, batch_id: _Optional[str] = ..., policy_version_id: _Optional[int] = ...) -> None: ...
