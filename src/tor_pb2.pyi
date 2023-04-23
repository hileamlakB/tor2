from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
ENTRY: NodeType
EXIT: NodeType
MIDDLE: NodeType
NONKEY: KeyType
NONNODE: NodeType
PRIVATE: KeyType
PUBLIC: KeyType

class AcceptKeyRequest(_message.Message):
    __slots__ = ["key", "key_type"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    key: str
    key_type: KeyType
    def __init__(self, key: _Optional[str] = ..., key_type: _Optional[_Union[KeyType, str]] = ...) -> None: ...

class AcceptKeyResponse(_message.Message):
    __slots__ = ["response"]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...

class GetRelayNodesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetRelayNodesResponse(_message.Message):
    __slots__ = ["relay_nodes"]
    RELAY_NODES_FIELD_NUMBER: _ClassVar[int]
    relay_nodes: _containers.RepeatedCompositeFieldContainer[RelayNode]
    def __init__(self, relay_nodes: _Optional[_Iterable[_Union[RelayNode, _Mapping]]] = ...) -> None: ...

class ProcessMessageRequest(_message.Message):
    __slots__ = ["encrypted_message", "next_relay_node"]
    ENCRYPTED_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NEXT_RELAY_NODE_FIELD_NUMBER: _ClassVar[int]
    encrypted_message: str
    next_relay_node: RelayNode
    def __init__(self, encrypted_message: _Optional[str] = ..., next_relay_node: _Optional[_Union[RelayNode, _Mapping]] = ...) -> None: ...

class ProcessMessageResponse(_message.Message):
    __slots__ = ["encrypted_message"]
    ENCRYPTED_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    encrypted_message: str
    def __init__(self, encrypted_message: _Optional[str] = ...) -> None: ...

class RelayNode(_message.Message):
    __slots__ = ["address", "node_type"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    address: str
    node_type: NodeType
    def __init__(self, address: _Optional[str] = ..., node_type: _Optional[_Union[NodeType, str]] = ...) -> None: ...

class RequestCircuitRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RequestCircuitResponse(_message.Message):
    __slots__ = ["relay_nodes"]
    RELAY_NODES_FIELD_NUMBER: _ClassVar[int]
    relay_nodes: _containers.RepeatedCompositeFieldContainer[RelayNode]
    def __init__(self, relay_nodes: _Optional[_Iterable[_Union[RelayNode, _Mapping]]] = ...) -> None: ...

class SendMessageRequest(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class SendMessageResponse(_message.Message):
    __slots__ = ["response"]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...

class KeyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class NodeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
