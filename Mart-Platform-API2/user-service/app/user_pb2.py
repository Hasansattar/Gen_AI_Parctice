# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\"\x8c\x01\n\x04User\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\r\n\x05phone\x18\x04 \x01(\t\x12\x11\n\tis_active\x18\x05 \x01(\x08\x12\x13\n\x0bis_verified\x18\x06 \x01(\x08\x12\x0c\n\x04role\x18\x07 \x01(\t\x12\x12\n\ncreated_at\x18\x08 \x01(\t\"\xbd\x01\n\nUserCreate\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x15\n\rpassword_hash\x18\x04 \x01(\t\x12\r\n\x05phone\x18\x05 \x01(\t\x12\x11\n\tis_active\x18\x06 \x01(\x08\x12\x13\n\x0bis_verified\x18\x07 \x01(\x08\x12\x0c\n\x04role\x18\x08 \x01(\t\x12\x12\n\ncreated_at\x18\t \x01(\t\x12\x12\n\nupdated_at\x18\n \x01(\t\"R\n\nUserUpdate\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x15\n\rpassword_hash\x18\x02 \x01(\t\x12\r\n\x05phone\x18\x03 \x01(\t\x12\x12\n\nupdated_at\x18\x04 \x01(\t\"\x18\n\nUserDelete\x12\n\n\x02id\x18\x01 \x01(\x05\"\x8d\x01\n\x0bUserProfile\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x04 \x01(\t\x12\x12\n\navatar_url\x18\x05 \x01(\t\x12\x15\n\rdate_of_birth\x18\x06 \x01(\t\x12\x0f\n\x07user_id\x18\x07 \x01(\x05\"\x93\x01\n\x11UserProfileCreate\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x04 \x01(\t\x12\x12\n\navatar_url\x18\x05 \x01(\t\x12\x15\n\rdate_of_birth\x18\x06 \x01(\t\x12\x0f\n\x07user_id\x18\x07 \x01(\x05\"k\n\x11UserProfileUpdate\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x04 \x01(\t\x12\x12\n\navatar_url\x18\x05 \x01(\t\"6\n\x10UserLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"Q\n\x11UserLoginResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x02 \x01(\t\x12\x15\n\rrefresh_token\x18\x03 \x01(\t\"R\n\x14PasswordResetRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x13\n\x0boldpassword\x18\x02 \x01(\t\x12\x13\n\x0bnewpassword\x18\x03 \x01(\t\"A\n\x14PasswordResetConfirm\x12\x13\n\x0breset_token\x18\x01 \x01(\t\x12\x14\n\x0cnew_password\x18\x02 \x01(\t\"\xbe\x01\n\tUserEvent\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12(\n\nevent_type\x18\x03 \x01(\x0e\x32\x14.UserEvent.EventType\x12\x15\n\revent_payload\x18\x04 \x01(\t\x12\x11\n\ttimestamp\x18\x05 \x01(\t\"@\n\tEventType\x12\x0b\n\x07\x43REATED\x10\x00\x12\x0b\n\x07UPDATED\x10\x01\x12\x0b\n\x07\x44\x45LETED\x10\x02\x12\x0c\n\x08VERIFIED\x10\x03\" \n\x08UserList\x12\x14\n\x05users\x18\x01 \x03(\x0b\x32\x05.User\"1\n\x0fUserProfileList\x12\x1e\n\x08profiles\x18\x01 \x03(\x0b\x32\x0c.UserProfileb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USER._serialized_start=15
  _USER._serialized_end=155
  _USERCREATE._serialized_start=158
  _USERCREATE._serialized_end=347
  _USERUPDATE._serialized_start=349
  _USERUPDATE._serialized_end=431
  _USERDELETE._serialized_start=433
  _USERDELETE._serialized_end=457
  _USERPROFILE._serialized_start=460
  _USERPROFILE._serialized_end=601
  _USERPROFILECREATE._serialized_start=604
  _USERPROFILECREATE._serialized_end=751
  _USERPROFILEUPDATE._serialized_start=753
  _USERPROFILEUPDATE._serialized_end=860
  _USERLOGINREQUEST._serialized_start=862
  _USERLOGINREQUEST._serialized_end=916
  _USERLOGINRESPONSE._serialized_start=918
  _USERLOGINRESPONSE._serialized_end=999
  _PASSWORDRESETREQUEST._serialized_start=1001
  _PASSWORDRESETREQUEST._serialized_end=1083
  _PASSWORDRESETCONFIRM._serialized_start=1085
  _PASSWORDRESETCONFIRM._serialized_end=1150
  _USEREVENT._serialized_start=1153
  _USEREVENT._serialized_end=1343
  _USEREVENT_EVENTTYPE._serialized_start=1279
  _USEREVENT_EVENTTYPE._serialized_end=1343
  _USERLIST._serialized_start=1345
  _USERLIST._serialized_end=1377
  _USERPROFILELIST._serialized_start=1379
  _USERPROFILELIST._serialized_end=1428
# @@protoc_insertion_point(module_scope)