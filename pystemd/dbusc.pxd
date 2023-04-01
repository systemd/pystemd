# cython: language_level=3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from libc.stdint cimport (
    int16_t,
    int32_t,
    int64_t,
    uint8_t,
    uint16_t,
    uint32_t,
    uint64_t,
)


cdef extern from "sys/uio.h":
    cdef struct iovec:
        void * iov_base
        size_t iov_len


cdef extern from "sys/syscall.h":
    int __NR_setns
    long syscall(long number, ...)


cdef extern from "systemd/sd-journal.h":
    int sd_journal_sendv(iovec *iov, int n);


cdef extern from "systemd/sd-daemon.h":
  int SD_LISTEN_FDS_START
  int sd_listen_fds(int unset_environment)
  int sd_notify(int unset_environment, const char *state)
  int sd_booted()
  int sd_watchdog_enabled(int unset_environment, uint64_t *usec)

cdef extern from "systemd/sd-bus.h":
  ctypedef struct sd_bus:
    pass

  ctypedef struct sd_bus_message:
    pass

  ctypedef struct sd_bus_slot:
    pass

  ctypedef struct sd_bus_error:
    char *name
    char *message
    int _need_free

  ctypedef int (*sd_bus_message_handler_t)(
    sd_bus_message *m,
    void *userdata,
    sd_bus_error *ret_error
  ) except -1

  int sd_bus_open_user(sd_bus **ret)
  int sd_bus_open_system(sd_bus **ret)
  int sd_bus_open_system_remote(sd_bus **ret, const char *host)
  int sd_bus_open_system_machine(sd_bus **ret, const char *machine)

  int sd_bus_default_user(sd_bus **ret)

  int sd_bus_new(sd_bus **ret)
  int sd_bus_set_address(sd_bus *bus, const char *address)
  int sd_bus_set_bus_client(sd_bus *bus, int b)
  int sd_bus_get_address(sd_bus *bus, const char **address)
  int sd_bus_start(sd_bus *ret)

  int sd_bus_call(sd_bus *bus, sd_bus_message *m, uint64_t usec, sd_bus_error *ret_error, sd_bus_message **reply)
  int sd_bus_call_method(
    sd_bus *bus,
    const char *destination,
    const char *path,
    const char *interface,
    const char *member,
    sd_bus_error *ret_error,
    sd_bus_message **reply,
    const char *types, ...)

  int sd_bus_get_property_string(
    sd_bus *bus,
    char *destination,
    char *path,
    char *interface,
    char *member,
    sd_bus_error *ret_error,
    char **ret)

  int sd_bus_get_property(
    sd_bus *bus,
    const char *destination,
    const char *path,
    const char *interface,
    const char *member,
    sd_bus_error *ret_error,
    sd_bus_message **reply,
    const char *type)

  int sd_bus_get_fd(sd_bus *bus)
  int sd_bus_get_unique_name(sd_bus *bus, const char **unique)
  int sd_bus_process(sd_bus *bus, sd_bus_message **r)
  int sd_bus_wait(sd_bus *bus, uint64_t timeout_usec)
  void sd_bus_error_free(sd_bus_error *e)
  sd_bus *sd_bus_unref(sd_bus *bus)
  void sd_bus_close(sd_bus *bus)

  int sd_bus_message_new_method_call(
    sd_bus *bus,
    sd_bus_message **m,
    const char *destination,
    const char *path,
    const char *interface,
    const char *member)

  int sd_bus_message_peek_type(
    sd_bus_message *m,
    char *type,
    const char **contents)

  int sd_bus_message_enter_container(sd_bus_message *m, char type, const char *contents)
  int sd_bus_message_exit_container(sd_bus_message *m)
  int sd_bus_message_open_container(sd_bus_message *m, char type, const char *contents)
  int sd_bus_message_close_container(sd_bus_message *m)
  int sd_bus_message_read(sd_bus_message *m, const char *types, ...)
  int sd_bus_message_read_basic(sd_bus_message *m, char type, void *p)
  int sd_bus_message_append(sd_bus_message *m, const char *types, ...)
  int sd_bus_message_append_array(sd_bus_message *m, char type, const void *ptr, size_t size)

  int sd_bus_message_is_signal(sd_bus_message *m, const char *interface, const char *member)
  int sd_bus_message_is_method_call(sd_bus_message *m, const char *interface, const char *member)
  int sd_bus_message_is_method_error(sd_bus_message *m, const char *name)
  int sd_bus_message_is_empty(sd_bus_message *m)

  int sd_bus_message_get_type(sd_bus_message *m, uint8_t *type)
  int sd_bus_message_get_cookie(sd_bus_message *m, uint64_t *cookie)
  int sd_bus_message_get_reply_cookie(sd_bus_message *m, uint64_t *cookie)
  int sd_bus_message_get_priority(sd_bus_message *m, int64_t *priority)

  int sd_bus_message_get_monotonic_usec(sd_bus_message *m, uint64_t *usec)
  int sd_bus_message_get_realtime_usec(sd_bus_message *m, uint64_t *usec)
  int sd_bus_message_get_seqnum(sd_bus_message *m, uint64_t* seqnum)

  const char *sd_bus_message_get_signature(sd_bus_message *m, int complete)
  const char *sd_bus_message_get_path(sd_bus_message *m)
  const char *sd_bus_message_get_interface(sd_bus_message *m)
  const char *sd_bus_message_get_member(sd_bus_message *m)
  const char *sd_bus_message_get_destination(sd_bus_message *m)
  const char *sd_bus_message_get_sender(sd_bus_message *m)

  sd_bus_message* sd_bus_message_ref(sd_bus_message *m)
  sd_bus_message* sd_bus_message_unref(sd_bus_message *m)

  int sd_bus_path_encode(char* prefix, char* external_id, char **ret_path)
  int sd_bus_path_decode(char* path, char* prefix, char **ret_external_id)

  int sd_bus_set_allow_interactive_authorization(sd_bus *bus, int b);
  int sd_bus_get_allow_interactive_authorization(sd_bus *bus);



cdef extern from "systemd/sd-bus-protocol.h":
  ctypedef enum:
    _SD_BUS_MESSAGE_TYPE_INVALID
    SD_BUS_MESSAGE_METHOD_CALL
    SD_BUS_MESSAGE_METHOD_RETURN
    SD_BUS_MESSAGE_METHOD_ERROR
    SD_BUS_MESSAGE_SIGNAL
    _SD_BUS_MESSAGE_TYPE_MAX

  ctypedef enum:
    _SD_BUS_TYPE_INVALID
    SD_BUS_TYPE_BYTE
    SD_BUS_TYPE_BOOLEAN
    SD_BUS_TYPE_INT16
    SD_BUS_TYPE_UINT16
    SD_BUS_TYPE_INT32
    SD_BUS_TYPE_UINT32
    SD_BUS_TYPE_INT64
    SD_BUS_TYPE_UINT64
    SD_BUS_TYPE_DOUBLE
    SD_BUS_TYPE_STRING
    SD_BUS_TYPE_OBJECT_PATH
    SD_BUS_TYPE_SIGNATURE
    SD_BUS_TYPE_UNIX_FD
    SD_BUS_TYPE_ARRAY
    SD_BUS_TYPE_VARIANT
    SD_BUS_TYPE_STRUCT
    SD_BUS_TYPE_STRUCT_BEGIN
    SD_BUS_TYPE_STRUCT_END
    SD_BUS_TYPE_DICT_ENTRY
    SD_BUS_TYPE_DICT_ENTRY_BEGIN
    SD_BUS_TYPE_DICT_ENTRY_END

cdef union basic_data:
  uint8_t u8;
  uint16_t u16;
  int16_t s16;
  uint32_t u32;
  int32_t s32;
  uint64_t u64;
  int64_t s64;
  double d64;
  const char *string;
  int i;


cdef extern from 'stdbool.h':
  pass

# We may not need this since this file is just to declare where things are.
IF LIBSYSTEMD_VERSION >= 237:
  include "dbusc_v237.pxi"
