# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tor.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ttor.proto\x12\x03tor\"\x17\n\x15RequestCircuitRequest\"=\n\x16RequestCircuitResponse\x12#\n\x0brelay_nodes\x18\x01 \x03(\x0b\x32\x0e.tor.RelayNode\"J\n\x12SendMessageRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\x12#\n\x0brelay_nodes\x18\x02 \x03(\x0b\x32\x0e.tor.RelayNode\"\'\n\x13SendMessageResponse\x12\x10\n\x08response\x18\x01 \x01(\t\"[\n\x15ProcessMessageRequest\x12\x19\n\x11\x65ncrypted_message\x18\x01 \x01(\t\x12\'\n\x0fnext_relay_node\x18\x02 \x01(\x0b\x32\x0e.tor.RelayNode\"3\n\x16ProcessMessageResponse\x12\x19\n\x11\x65ncrypted_message\x18\x01 \x01(\t\"\x16\n\x14GetRelayNodesRequest\"<\n\x15GetRelayNodesResponse\x12#\n\x0brelay_nodes\x18\x01 \x03(\x0b\x32\x0e.tor.RelayNode\"R\n\tRelayNode\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x12\n\npublic_key\x18\x02 \x01(\t\x12 \n\tnode_type\x18\x03 \x01(\x0e\x32\r.tor.NodeType*+\n\x08NodeType\x12\t\n\x05\x45NTRY\x10\x00\x12\n\n\x06MIDDLE\x10\x01\x12\x08\n\x04\x45XIT\x10\x02\x32\x99\x01\n\x06\x43lient\x12K\n\x0eRequestCircuit\x12\x1a.tor.RequestCircuitRequest\x1a\x1b.tor.RequestCircuitResponse\"\x00\x12\x42\n\x0bSendMessage\x12\x17.tor.SendMessageRequest\x1a\x18.tor.SendMessageResponse\"\x00\x32T\n\x05Relay\x12K\n\x0eProcessMessage\x12\x1a.tor.ProcessMessageRequest\x1a\x1b.tor.ProcessMessageResponse\"\x00\x32[\n\x0f\x44irectoryServer\x12H\n\rGetRelayNodes\x12\x19.tor.GetRelayNodesRequest\x1a\x1a.tor.GetRelayNodesResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tor_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NODETYPE._serialized_start=539
  _NODETYPE._serialized_end=582
  _REQUESTCIRCUITREQUEST._serialized_start=18
  _REQUESTCIRCUITREQUEST._serialized_end=41
  _REQUESTCIRCUITRESPONSE._serialized_start=43
  _REQUESTCIRCUITRESPONSE._serialized_end=104
  _SENDMESSAGEREQUEST._serialized_start=106
  _SENDMESSAGEREQUEST._serialized_end=180
  _SENDMESSAGERESPONSE._serialized_start=182
  _SENDMESSAGERESPONSE._serialized_end=221
  _PROCESSMESSAGEREQUEST._serialized_start=223
  _PROCESSMESSAGEREQUEST._serialized_end=314
  _PROCESSMESSAGERESPONSE._serialized_start=316
  _PROCESSMESSAGERESPONSE._serialized_end=367
  _GETRELAYNODESREQUEST._serialized_start=369
  _GETRELAYNODESREQUEST._serialized_end=391
  _GETRELAYNODESRESPONSE._serialized_start=393
  _GETRELAYNODESRESPONSE._serialized_end=453
  _RELAYNODE._serialized_start=455
  _RELAYNODE._serialized_end=537
  _CLIENT._serialized_start=585
  _CLIENT._serialized_end=738
  _RELAY._serialized_start=740
  _RELAY._serialized_end=824
  _DIRECTORYSERVER._serialized_start=826
  _DIRECTORYSERVER._serialized_end=917
# @@protoc_insertion_point(module_scope)
