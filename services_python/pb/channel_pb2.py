# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: channel.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rchannel.proto\x12\x05proto\"\x1f\n\x11GetChannelRequest\x12\n\n\x02id\x18\x01 \x01(\t\"t\n\x12GetChannelResponse\x12\x31\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32#.proto.GetChannelResponse.DataEntry\x1a+\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32U\n\x0e\x43hannelService\x12\x43\n\nGetChannel\x12\x18.proto.GetChannelRequest\x1a\x19.proto.GetChannelResponse\"\x00\x42\x06Z\x04./pbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'channel_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\004./pb'
  _globals['_GETCHANNELRESPONSE_DATAENTRY']._options = None
  _globals['_GETCHANNELRESPONSE_DATAENTRY']._serialized_options = b'8\001'
  _globals['_GETCHANNELREQUEST']._serialized_start=24
  _globals['_GETCHANNELREQUEST']._serialized_end=55
  _globals['_GETCHANNELRESPONSE']._serialized_start=57
  _globals['_GETCHANNELRESPONSE']._serialized_end=173
  _globals['_GETCHANNELRESPONSE_DATAENTRY']._serialized_start=130
  _globals['_GETCHANNELRESPONSE_DATAENTRY']._serialized_end=173
  _globals['_CHANNELSERVICE']._serialized_start=175
  _globals['_CHANNELSERVICE']._serialized_end=260
# @@protoc_insertion_point(module_scope)
