# cython: language_level=3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import os

cimport pystemd.dbusc as dbusc

from pprint import pformat

from pystemd.dbusexc import DBusError
from pystemd.utils import x2char_star

from libc.stdint cimport (
    int16_t,
    int32_t,
    int64_t,
    uint8_t,
    uint16_t,
    uint32_t,
    uint64_t,
)
from libc.stdlib cimport free
from libcpp cimport bool

CONTAINER_TYPES = (
  dbusc.SD_BUS_TYPE_ARRAY,
  dbusc.SD_BUS_TYPE_VARIANT,
  dbusc.SD_BUS_TYPE_STRUCT,
  dbusc.SD_BUS_TYPE_DICT_ENTRY
)

class VariableReturn(object):
  def __init__(self, parent=None, v_type=None):
    self.data = []
    self.parent = parent
    self.v_type = v_type

  def create_child(self, v_type=None):
    self.data.append(
      VariableReturn(
        parent=self,
        v_type=v_type))

    return self.data[-1]

  def append(self, dt):
    self.data.append(dt)

  def dump(self):
    o = [
      e.dump() if isinstance(e, VariableReturn) else e
      for e in self.data
    ]
    if self.v_type == dbusc.SD_BUS_TYPE_STRUCT:
      return tuple(o)
    elif self.v_type == dbusc.SD_BUS_TYPE_VARIANT:
      return o[0]
    elif self.v_type == dbusc.SD_BUS_TYPE_DICT_ENTRY:
      return {o[0]: o[1]}
    elif self.v_type == dbusc.SD_BUS_TYPE_ARRAY and o and isinstance(o[0], dict):
      return dict(e for d in o for e in d.items())
    return o


cdef class DbusMessage:
    cdef dbusc.sd_bus_message *_msg

    cdef public body
    cdef public dict headers

    def __dealloc__(self):
      dbusc.sd_bus_message_unref(self._msg)

    cdef dbusc.sd_bus_message **ref(self):
        return &(self._msg)

    cdef dbusc.sd_bus_message *msg(self):
        return self._msg

    cdef set_bus_message(self, dbusc.sd_bus_message *msg):
        assert self._msg == NULL
        self._msg = msg
        dbusc.sd_bus_message_ref(msg)

    cpdef process_reply(self, bool with_headers):
        """
          Read through a sd_bus_message reply object and return the answer to that call.
          It's loosely based on bus_message_dump in \
          https://github.com/systemd/systemd/blob/master/src/libsystemd/sd-bus/bus-dump.c
          except that will dump to stdout, this will give you a nice python array (you
          are welcome!).

          The nice thing about this method, is that it will enter complex types like
          arrays or struct. so if the answer is in the form of "a(sbi)", it can return
          as an answer [[b'a', True, 0], [b'b', False, 1], ...]
        """
        cdef:
            int r
            uint8_t msg_type
            char peek_type
            const char *peek_contents = NULL
            dbusc.basic_data rettype

        return_e = VariableReturn()

        while True:
            r = dbusc.sd_bus_message_peek_type(self._msg, &peek_type, &peek_contents)

            if r < 0:
              # e.g. an empty DbusMessage: peek_type was not set
              raise DBusError(r, None, "Failed to read message type")

            if r == 0:
              if return_e.parent is None:
                break

              r = dbusc.sd_bus_message_exit_container(self._msg)

              if r < 0:
                raise DBusError(r, None, "Failed to exit container")

              return_e = return_e.parent
              continue

            if peek_type in CONTAINER_TYPES:
              return_e = return_e.create_child(v_type=peek_type)
              r = dbusc.sd_bus_message_enter_container(self._msg, peek_type, peek_contents)

              if r < 0:
                raise DBusError(r, None, "Failed to enter container")

              continue

            r = dbusc.sd_bus_message_read_basic(self._msg, peek_type, &rettype)

            if r < 0:
              raise DBusError(r, None, "Failed to read message")

            return_e.append(cast_data_to(rettype, peek_type))

        u = return_e.dump()

        if len(u) > 1:
          self.body = u
        elif u:
          self.body = u[0]
        else:
          self.body = None

        # get the headers

        if with_headers:
            msg_type = self.get_type()
            if msg_type == dbusc.SD_BUS_MESSAGE_SIGNAL:
                self.headers = {
                    'Type': msg_type,
                    'Typename': 'signal',
                    #'Endian': None,
                    #'Flags': None,
                    #'Version': None,
                    'Priority': self.get_priority(),
                    'Cookie': self.get_cookie(),
                    'ReplyCookie': None,

                    'Sender':self.get_sender(),
                    'Destination': None,
                    'Path': self.get_path(),
                    'Interface': self.get_interface(),
                    'Member': self.get_member(),

                }
            elif msg_type == dbusc.SD_BUS_MESSAGE_METHOD_CALL:
                self.headers = {
                    'Type': msg_type,
                    'Typename': 'method_call',
                    #'Endian': None,
                    #'Flags': None,
                    #'Version': None,
                    'Priority': self.get_priority(),
                    'Cookie': self.get_cookie(),
                    'ReplyCookie': None,

                    'Sender':self.get_sender(),
                    'Destination': self.get_destination(),
                    'Path': self.get_path(),
                    'Interface': self.get_interface(),
                    'Member': self.get_member(),

                }
            elif msg_type == dbusc.SD_BUS_MESSAGE_METHOD_RETURN:
                self.headers = {
                    'Type': msg_type,
                    'Typename': 'method_return',
                    #'Endian': None,
                    #'Flags': None,
                    #'Version': None,
                    'Priority': self.get_priority(),
                    'Cookie': self.get_cookie(),
                    'ReplyCookie': self.get_reply_cookie(),

                    'Sender':self.get_sender(),
                    'Destination': self.get_destination(),
                    'Path': None,
                    'Interface': None,
                    'Member': None,

                }
            else:
                self.headers = {
                    'Type': msg_type,
                    'Typename': 'Unknown',
                    #'Endian': None,
                    #'Flags': None,
                    #'Version': None,
                    'Priority': None,
                    'Cookie': None,
                    'ReplyCookie': None,

                    'Sender': None,
                    'Destination': None,
                    'Path': None,
                    'Interface': None,
                    'Member': None,

                }

    # interfaces to sd_bus_message
    # this will mostly be available to python also

    cpdef bool is_empty(self):
        return dbusc.sd_bus_message_is_empty(self._msg)

    cpdef bool is_signal(self, const char *interface, const char *member):
        return dbusc.sd_bus_message_is_signal(self._msg, interface, member) > 0


    cpdef uint8_t get_type(self):
        cdef uint8_t ret = 0
        dbusc.sd_bus_message_get_type(self._msg, &ret)
        return ret


    cpdef uint64_t get_cookie(self):
        cdef uint64_t ret = 0
        dbusc.sd_bus_message_get_cookie(self._msg, &ret)
        return ret


    cpdef uint64_t get_reply_cookie(self):
        cdef uint64_t ret = 0
        dbusc.sd_bus_message_get_reply_cookie(self._msg, &ret)
        return ret

    cpdef int64_t get_priority(self):
        cdef int64_t ret = 0
        dbusc.sd_bus_message_get_priority(self._msg, &ret)
        return ret

    # These header fields are optional (a method reply has no path, interface
    # or member), and sd-bus returns NULL for a missing one: return None.

    cpdef object get_path(self):
        return _c2b(dbusc.sd_bus_message_get_path(self._msg))

    cpdef object get_interface(self):
        return _c2b(dbusc.sd_bus_message_get_interface(self._msg))

    cpdef object get_member(self):
        return _c2b(dbusc.sd_bus_message_get_member(self._msg))

    cpdef object get_destination(self):
        return _c2b(dbusc.sd_bus_message_get_destination(self._msg))

    cpdef object get_sender(self):
        return _c2b(dbusc.sd_bus_message_get_sender(self._msg))


cdef class DBus:
    cdef dbusc.sd_bus *bus
    cdef bool user_mode
    cdef int interactive
    # (callback, userdata) for every match_signal: sd-bus only holds a
    # borrowed pointer to them, so they must live as long as the bus does
    cdef list _signal_callbacks

    def __cinit__(self, *args, **kwargs):
      # set here, not in __init__, so subclasses that don't call
      # super().__init__ still get them
      self.interactive = -1
      self._signal_callbacks = []

    def __init__(self, user_mode=False, interactive=None):
      self.user_mode = user_mode
      self.interactive = -1 if interactive is None else int(interactive)

    def __dealloc__(self):
      self._free_bus()

    cdef _free_bus(self):
      if self.bus != NULL:
        dbusc.sd_bus_close(self.bus)
        dbusc.sd_bus_unref(self.bus)
        self.bus = NULL

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *errs):
        self.close()

    cdef int open_dbus_bus(self):
      cdef int r
      # if user_mode not set, then this is easy:
      if not self.user_mode:
        return dbusc.sd_bus_open_system(&(self.bus))
      else:
        return dbusc.sd_bus_open_user(&(self.bus))

    def open(self):
        cdef int rets
        cdef bint was_closed = self.bus == NULL
        rets = self.open_dbus_bus()
        if (rets < 0):
            if was_closed:
                # DBusAddress may have created the bus before failing
                self._free_bus()
            raise DBusError(rets, None, "Could not open a bus to DBus")
        if self.interactive >= 0:
            self.set_allow_interactive_authorization(self.interactive)

    def close(self):
        """
        Close the connection. Closing twice is a no-op; using the bus after
        closing it raises DBusError (sd-bus answers ENOTCONN) until it is
        opened again.
        """
        self._free_bus()
        self._signal_callbacks = []

    def process(self):
        cdef:
            int r
            DbusMessage msg = DbusMessage()

        r = dbusc.sd_bus_process(self.bus, msg.ref())
        if r < 0:
            raise DBusError(r, None, "Failed to process bus")

        return msg

    cdef _msg_append(
        self, dbusc.sd_bus_message *msg_call, int arg_type_i, arg_value):

      cdef int r
      cdef char * arg_type_c = NULL
      cdef char arg_type = <char>arg_type_i

      if 0 < arg_type_i < 128:
          inter = chr(arg_type_i).encode()
          arg_type_c = inter
      elif arg_type_i != -1:
          raise DBusError(
            -42, None, "Unknown arg type %s for %s" % (arg_type_i, arg_value))

      if arg_type == dbusc.SD_BUS_TYPE_BYTE:
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <uint8_t>arg_value)
      elif arg_type == dbusc.SD_BUS_TYPE_BOOLEAN:
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <bool>arg_value)
      elif arg_type == dbusc.SD_BUS_TYPE_INT16:
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <int16_t>arg_value)
      elif arg_type == dbusc.SD_BUS_TYPE_UINT16:
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <uint16_t>arg_value)
      elif arg_type == dbusc.SD_BUS_TYPE_INT32:
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <int32_t>arg_value)
      elif arg_type == dbusc.SD_BUS_TYPE_UINT32:
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <uint32_t>arg_value)
      elif arg_type == dbusc.SD_BUS_TYPE_INT64:
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <int64_t>arg_value)
      elif arg_type == dbusc.SD_BUS_TYPE_UINT64:
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <uint64_t>arg_value)
      elif arg_type == dbusc.SD_BUS_TYPE_DOUBLE:
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <double>arg_value)
      elif arg_type in (
          dbusc.SD_BUS_TYPE_STRING, dbusc.SD_BUS_TYPE_OBJECT_PATH,
          dbusc.SD_BUS_TYPE_SIGNATURE):
        carg_value = x2char_star(arg_value)
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <char*>carg_value)
      elif arg_type == dbusc.SD_BUS_TYPE_UNIX_FD:
        r = dbusc.sd_bus_message_append(
          msg_call,
          arg_type_c,
          <int>arg_value)
      elif arg_type in CONTAINER_TYPES: # open container
        r = dbusc.sd_bus_message_open_container(
          msg_call,
          arg_type,
          <char*>arg_value)
      elif arg_type_i == -1: # close container
        r = dbusc.sd_bus_message_close_container(msg_call)
      else:
        raise DBusError(
          -42, None, "Unknown arg type %s for %s" % (arg_type, arg_value))

      if r < 0:
        raise DBusError(
          r, None, "Failed to append %r (type %r) to the message" % (
            arg_value, chr(arg_type_i) if arg_type_i > 0 else "end of container"))

    def call_method(
            self,
            const char *destination,
            const char *path,
            const char *interface,
            const char *method,
            args):

        cdef:
            int r
            int arg_type

            dbusc.sd_bus_message *msg_call = NULL
            dbusc.sd_bus_message *msg_reply = NULL
            dbusc.sd_bus_error error = dbusc.sd_bus_error(NULL, NULL, 0)

            DbusMessage msg = DbusMessage()

        r = dbusc.sd_bus_message_new_method_call(
            self.bus,
            &msg_call,
            destination,
            path,
            interface,
            method
        )

        if r < 0:
            raise DBusError(r, None, 'Could not create DBus method')

        for narg, (arg_type, arg_value) in enumerate(args or []):
            try:
                self._msg_append(msg_call, arg_type, arg_value)
            except TypeError as e:
              raise TypeError(
                str(e) + ' for input "{}", element '
                'number {} in input series:\n{}'.format(
                  arg_value, narg, pformat(args)))


        r = dbusc.sd_bus_call(self.bus, msg_call, 0, &error, msg.ref())

        if r < 0:
            raise DBusError(r, error.name, error.message)

        msg.process_reply(False)

        dbusc.sd_bus_message_unref(msg_call)
        dbusc.sd_bus_message_unref(msg_reply)
        dbusc.sd_bus_error_free(&error)

        return msg


    def get_property(self,
            const char *destination,
            const char *path,
            const char *interface,
            const char *property,
            const char *rtype):

        cdef:
          int r
          dbusc.sd_bus_error error = dbusc.sd_bus_error(NULL, NULL, 0)

          DbusMessage msg = DbusMessage()

        r = dbusc.sd_bus_get_property(
          self.bus,
          destination,
          path,
          interface,
          property,
          &error,
          msg.ref(),
          rtype
        )

        if r < 0:
            raise DBusError(r, error.name, error.message)

        msg.process_reply(False)
        return msg.body

    def match_signal(
      self,
      sender,
      path,
      interface,
      member,
      callback,
      userdata=None
    ):
      """
      This method will register a <callback> (a python function) when the signal
      <member> on <interface> is trigger for the specify interface. An example
      on how to use it can be found in
      https://github.com/systemd/pystemd/blob/master/examples/monitor.py
      """

      IF LIBSYSTEMD_VERSION < 237:
          raise DBusError(-1, None, "sd_bus_match_signal not available in libsystemd v%d" % LIBSYSTEMD_VERSION)
      ELSE:
          cdef int r

          # sd-bus gets a borrowed pointer: keep the tuple alive with the bus
          handler_data = (callback, userdata)

          r = dbusc.sd_bus_match_signal(
            self.bus,
            NULL,
            _b2c(x2char_star(sender)),
            _b2c(x2char_star(path)),
            _b2c(x2char_star(interface)),
            _b2c(x2char_star(member)),
            match_signal_callback_handler,
            <void*> handler_data
          )

          if r < 0:
              raise DBusError(r, None, "Failed to add signal match")

          self._signal_callbacks.append(handler_data)

    # Direct interface to sd_bus_<methods>

    cpdef wait(self, uint64_t timeout):
        cdef int r = dbusc.sd_bus_wait(self.bus, timeout)
        if r < 0:
            raise DBusError(r, None, "Failed to wait for bus")

    cpdef const char* get_unique_name(self):
        cdef:
            int r
            const char *unique_name

        r = dbusc.sd_bus_get_unique_name(self.bus, &unique_name)

        if r < 0:
            raise DBusError(r, None, "Failed to get unique name")

        return unique_name

    cpdef int get_fd(self):
      return dbusc.sd_bus_get_fd(self.bus)

    cpdef bool get_allow_interactive_authorization(self):
      return dbusc.sd_bus_get_allow_interactive_authorization(self.bus)

    cpdef set_allow_interactive_authorization(self, bool interactive):
        r = dbusc.sd_bus_set_allow_interactive_authorization(self.bus, interactive)
        if r < 0:
            raise DBusError(r, None, "Failed to set interactive authorization")


cdef class DBusMachine(DBus):
  "DBus class that connects to machine"
  # bytes, not char*: a char* would point into whatever (possibly temporary)
  # bytes object was passed to __init__
  cdef bytes machine

  def __init__(self, machine):
    super().__init__()
    self.machine = x2char_star(machine)

  cdef int open_dbus_bus(self):
    return dbusc.sd_bus_open_system_machine(&(self.bus), self.machine)


cdef class DBusRemote(DBus):
  """
  DBus class that connects to a remote host, this is using ssh, 
  this uses [sd_bus_open_system_remote](https://manpages.debian.org/testing/libsystemd-dev/sd_bus_open_system_remote.3.en.html)
  that will:

    connects to the system bus on the specified host using ssh(1). host consists of an optional user name followed by the "@" symbol, 
    and the hostname, optionally followed by a ":" and a port, optionally followed by a "/" and a machine name. If the machine name is 
    given, a connection is created to the system bus in the specified container on the remote machine, and otherwise a connection to 
    the system bus on the specified host is created.
  """

  cdef bytes host

  def __init__(self, host):
    super().__init__()
    self.host = x2char_star(host)

  cdef int open_dbus_bus(self):
    return dbusc.sd_bus_open_system_remote(&(self.bus), self.host)

cdef class DBusAddress(DBus):
  "DBus class that connects to custom address"
  cdef bytes address
  cdef bint peer_to_peer

  def __init__(self, address, peer_to_peer=False):
    self.address = bytes(address)
    self.peer_to_peer = int(peer_to_peer)

  cdef int open_dbus_bus(self):
    r = dbusc.sd_bus_new(&(self.bus))
    if r < 0:
      return r
    r = dbusc.sd_bus_set_address(self.bus, self.address)

    if r < 0:
        return r

    if not self.peer_to_peer:
      r = dbusc.sd_bus_set_bus_client(self.bus, 1)
      if r < 0:
        return r

    r = dbusc.sd_bus_start(self.bus);
    if r < 0:
      return r

    return 0


cdef cast_data_to(dbusc.basic_data basic, cast_type):
  """
  Get the right casting out of a union, the union type and values can be found
  in: https://www.freedesktop.org/software/systemd/man/sd_bus_message_append.html
  or https://dbus.freedesktop.org/doc/dbus-specification.html#type-system (i
  like the first one more than the second one)
  """
  if cast_type == dbusc.SD_BUS_TYPE_BYTE:
    return basic.u8
  elif cast_type == dbusc.SD_BUS_TYPE_BOOLEAN:
    return <bool>basic.i
  elif cast_type == dbusc.SD_BUS_TYPE_INT16:
    return basic.s16
  elif cast_type == dbusc.SD_BUS_TYPE_UINT16:
    return basic.u16
  elif cast_type == dbusc.SD_BUS_TYPE_INT32:
    return basic.s32
  elif cast_type == dbusc.SD_BUS_TYPE_UINT32:
    return basic.u32
  elif cast_type == dbusc.SD_BUS_TYPE_INT64:
    return basic.s64
  elif cast_type == dbusc.SD_BUS_TYPE_UINT64:
    return basic.u64
  elif cast_type == dbusc.SD_BUS_TYPE_DOUBLE:
    return basic.d64
  elif cast_type == dbusc.SD_BUS_TYPE_STRING:
    return basic.string
  elif cast_type == dbusc.SD_BUS_TYPE_OBJECT_PATH:
    return basic.string
  elif cast_type == dbusc.SD_BUS_TYPE_SIGNATURE:
    return basic.string
  elif cast_type == dbusc.SD_BUS_TYPE_UNIX_FD:
    return basic.i

# Parsing argument library

cpdef int find_closure(char* args, char open, char close) except -1:
  cdef int counter = 0
  cdef int n
  cdef char arg

  for n, arg in enumerate(args):
    if arg == open:
      counter += 1
    elif arg == close:
      counter -= 1

    if counter == 0:
      return n

  raise ValueError(
    "unbalanced %r in signature %r" % (chr(open) + chr(close), args))


cdef dict COMPILE_METHODS

def compile_simple(char *arg):
  cdef char res = arg[0]
  cdef char *off = &res

  def process_simple(v):
    return [(res, v)]

  return off, process_simple

def compile_array(char *args):
  cdef char array_type = args[1]

  off, pr = COMPILE_METHODS.get(array_type, compile_simple)(args[1:])

  def process_array(v):
    cdef list ret = [(dbusc.SD_BUS_TYPE_ARRAY, off[1:])]
    for i in v:
        ret.extend(pr(i))
    ret.append((-1, None))
    return ret

  off = <char*>b'a' + off
  return off, process_array

def compile_struct(char *args):
  cdef int closing

  closing = find_closure(
    args, dbusc.SD_BUS_TYPE_STRUCT_BEGIN, dbusc.SD_BUS_TYPE_STRUCT_END)

  struc_extend = args[1:closing]

  cs = compile_args(struc_extend)

  def process_struct(v):
    return (
      [(dbusc.SD_BUS_TYPE_STRUCT, struc_extend)] +
      apply_args(cs, list(v)) +
      [(-1, None)]
    )
  return b'(' + struc_extend + b')', process_struct


COMPILE_METHODS = {
  dbusc.SD_BUS_TYPE_ARRAY: compile_array,
  dbusc.SD_BUS_TYPE_STRUCT_BEGIN: compile_struct,
}


cpdef list compile_args(char *args):
  cdef:
    int i = 0
    int size_of_args = len(args)
    char val
    list ret = []

  while i < size_of_args:
    val = args[i]
    off, pr = COMPILE_METHODS.get(val, compile_simple)(args[i:])

    ret.append(pr)
    i += len(off)

  return ret

cpdef list apply_args(list args, list values):
  cdef list ret = []
  for cfunc, value in zip(args, values):
    ret.extend(cfunc(value))
  return ret

cpdef list apply_signature(char *signature, list values):
  cdef list args = compile_args(signature)
  cdef list ret = []
  for cfunc, value in zip(args, values):
    ret.extend(cfunc(value))
  return ret


cpdef bytes path_encode(char* prefix,  char* external_id):
  """Python wrapper for sd_bus_path_encode, it produce a encoded version of a
  systemd path:

  example:

  In [1]: path_encode(b'/org/freedesktop/systemd1/unit', b'postfix.service')
  Out[1]: b'/org/freedesktop/systemd1/unit/postfix_2eservice'

  cdocs: https://www.freedesktop.org/software/systemd/man/sd_bus_path_encode.html
  """

  cdef:
    char* ret_path = NULL
    int r

  try:
    r = dbusc.sd_bus_path_encode(prefix, external_id, &ret_path)

    if r < 0:
      return b''

    return ret_path
  finally:
    free(ret_path)


cpdef bytes path_decode(char* path,  char* prefix):
  """Python wrapper for sd_bus_path_decode, it produce a decoded version of a
  systemd path:

  example:

  In [1]: path_decode(
  ...    b'/org/freedesktop/systemd1/unit/postfix_2eservice',
  ...    b'/org/freedesktop/systemd1/unit')
  Out[1]: b'postfix.service'

  cdocs: https://www.freedesktop.org/software/systemd/man/sd_bus_path_encode.html
  """

  cdef:
    char* answer = NULL
    int r

  try:
    r = dbusc.sd_bus_path_decode(path, prefix, &answer)

    if r <= 0:
      return b''

    return answer
  finally:
    free(answer)


cdef int match_signal_callback_handler(
  dbusc.sd_bus_message *m,
  void *userdata,
  dbusc.sd_bus_error *ret_error
) except -1:
  cdef:
    DbusMessage msg = DbusMessage()
    object mycallback
    object mydata

  mycallback, mydata = <object> userdata
  msg.set_bus_message(m)

  # We can't surface any Exception mycallback may throw, because this is
  # happening as a CALLBACK and we have no access to the caller of this method.
  # This will eventually be resolve into whatever exception the caller decide
  # to raise, usually SystemError
  mycallback(msg, error=None, userdata=mydata)

  return 0


cdef object _c2b(const char *value):
  "char* to bytes, None for NULL (converting NULL to bytes would crash)"
  if value == NULL:
    return None
  return <bytes>value


cdef char* _b2c(bytes py_value):
  "Interface to convert byte (as return by x2char_star) to char* respecting Null"
  cdef char * output = NULL

  if py_value is not None:
    output = py_value

  return output
