# cython: language_level=3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#


from libc.stdint cimport uint64_t
from libc.stdlib cimport free, malloc

cimport pystemd.dbusc as dbusc

from pystemd.utils import x2char_star

LISTEN_FDS_START = dbusc.SD_LISTEN_FDS_START

class PystemdDaemonError(Exception):
  "generic daemon error"


def listen_fds(int unset_environment=0):
  return dbusc.sd_listen_fds(unset_environment)


def listen_fds_with_names(int unset_environment=0):
  """
  interface to systemd sd_listen_fds_with_names: the file descriptors passed
  to us (socket activation, or the file descriptor store handing back what we
  stored with FDSTORE=1), as a dict of {name: [fd, ...]}. fds start at
  LISTEN_FDS_START; names come from FileDescriptorName= / FDNAME=.

  Names are not unique: a socket unit with several ListenStream= passes all
  its fds under the same name, and FDNAME= can be reused; hence the lists.

  usage:
    * `fd = pystemd.daemon.listen_fds_with_names()["db"][0]`
    * `for fd in pystemd.daemon.listen_fds_with_names().get("web.socket", []): ...`
  """
  cdef char **names = NULL
  cdef int n = dbusc.sd_listen_fds_with_names(unset_environment, &names)
  if n < 0:
    raise PystemdDaemonError(f"sd_listen_fds_with_names failed: {n}")

  fds = {}
  try:
    for i in range(n):
      name = names[i].decode() if names != NULL else "unknown"
      fds.setdefault(name, []).append(LISTEN_FDS_START + i)
    return fds
  finally:
    if names != NULL:
      for i in range(n):
        free(names[i])
      free(names)


def notify(int unset_environment, *states, fds=None, **kwstates):
  """
  interface to systemd sd_notify,

  params:
    unset_environment[int] = 1 if we should remove the notify information,
      otherwise 0.
    states/kwstates = array with states statements that are 'IDENTIFIER=VALUE'.
      e.g: 'READY=1' or keywords states like `ready=1`
      (This will be clear in usage).
    fds = optional file descriptor, or list of them (ints, or objects with a
      fileno() method), to send along with the message (sd_pid_notify_with_fds). Mostly
      for the file descriptor store: with `fdstore=1` systemd keeps them while
      the service restarts and hands them back on the next start (see
      listen_fds_with_names); the unit needs FileDescriptorStoreMax= > 0.

  usage:
    * `pystemd.daemon.notify(1, ready=1)`: this will signal `READY=1` to systemd
      notify and will remove all information from the environment. You should not
      try to talk to systemd notify socket again.
    *  `pystemd.daemon.notify(True, "READY=1")`: same as above just passed as a
      string.
    *  `pystemd.daemon.notify(False, ready=1, status='gime gime gime')`: will
      signal systemd that the app is ready and also set the status to
      'gime gime gime'. This command does not clean the notify environment.
    *  `pystemd.daemon.notify(False, fds=[memfd], fdstore=1, fdname="db")`:
      ask systemd to keep `memfd` for us, under the name "db".

    For info on sd_notify, check https://github.com/systemd/systemd/blob/\
master/src/systemd/sd-daemon.h#L173-L232

  """
  state = _join_states(states, kwstates)
  if fds is None:
    return dbusc.sd_notify(unset_environment, state)

  fd_list = _fd_list(fds)
  if not fd_list:
    return dbusc.sd_notify(unset_environment, state)

  cdef unsigned n_fds = len(fd_list)
  cdef int *c_fds = <int *> malloc(n_fds * sizeof(int))
  if c_fds == NULL:
    raise MemoryError()

  try:
    for i, fd in enumerate(fd_list):
      c_fds[i] = fd
    return dbusc.sd_pid_notify_with_fds(0, unset_environment, state, c_fds, n_fds)
  finally:
    free(c_fds)


def store_fd(name, fds, unset_environment=False, **kwstates):
  """
  hand `fds` (a single fd or a list; ints or objects with fileno()) to
  systemd's file descriptor store under `name`: systemd keeps them while the
  service restarts, and listen_fds_with_names()[name] gives them back on the
  next start. The unit needs FileDescriptorStoreMax= > 0.

  Same as notify(unset_environment, fds=fds, fdstore=1, fdname=name, **kwstates).

  usage:
    * `pystemd.daemon.store_fd("db", memfd)`
    * `pystemd.daemon.store_fd("listener", sock, ready=1)`
  """
  _check_fdname(name)
  return notify(unset_environment, fds=fds, fdstore=1, fdname=name, **kwstates)


def store_fds(fds_by_name, unset_environment=False, **kwstates):
  """
  store_fd() for several names at once: `fds_by_name` is {name: fds}, where
  fds is a single fd or a list. One FDNAME= covers a whole notify message,
  so this sends one message per name (not atomically). `unset_environment`
  and the extra states (e.g. ready=1) only go with the last message.
  Returns the lowest notify() result (negative errno if any send failed).

  usage:
    * `pystemd.daemon.store_fds({"listener": sock, "log": memfd}, ready=1)`
    * `pystemd.daemon.store_fds({...}, True)` or `store_fds({...}, unset_environment=True)`
  """
  items = list(fds_by_name.items())
  for name, _ in items:
    _check_fdname(name)
  if not items:
    return notify(unset_environment, **kwstates) if kwstates else 0

  results = [store_fd(name, fds) for name, fds in items[:-1]]
  name, fds = items[-1]
  results.append(store_fd(name, fds, unset_environment=unset_environment, **kwstates))
  return min(results)


def _check_fdname(name):
  # systemd ignores invalid names *silently* (the fds are just not stored),
  # so fail here instead: LISTEN_FDNAMES is ':'-separated, printable ASCII.
  if (
    not isinstance(name, str) or not 0 < len(name) <= 255
    or ":" in name or not all(32 <= ord(c) < 127 for c in name)
  ):
    raise ValueError(f"invalid fd name {name!r}: 1-255 printable ASCII characters, no ':'")


def _fd_list(fds):
  """
  normalize notify()'s `fds`: a single fd (int, or object with fileno()) or an
  iterable of them, to a list of ints.
  """
  if isinstance(fds, (str, bytes, bytearray)):
    # bytes would iterate as ints, silently sending the wrong fds
    raise TypeError(f"fds must be a file descriptor or a list of them, not {type(fds).__name__}")
  if isinstance(fds, int) or hasattr(fds, "fileno"):
    fds = [fds]

  fd_list = []
  for fd in fds:
    if isinstance(fd, int):
      fd_list.append(fd)
    elif hasattr(fd, "fileno"):
      fd_list.append(fd.fileno())
    else:
      raise TypeError(f"not a file descriptor: {fd!r} (expected an int or an object with fileno())")
  return fd_list


def _join_states(states, kwstates):
  pystates = [x2char_star(s) for s in states]
  pystates.extend(
    b'='.join([x2char_star(k.upper()), x2char_star(v, convert_all=True)])
    for k, v in kwstates.items()
  )
  return b'\n'.join(pystates)


def booted():
  "Returns True if system was booted with systemd"
  cdef int status = dbusc.sd_booted()
  if status >=0:
    return status > 0

  raise PystemdDaemonError("Could not get systemd booted status")


def watchdog_enabled(int unset_environment=0):
  """
  returns 0 if watchdog is not enabled, and returns the number of usec between
  keep-alive notification messages that the service manager expects.
  """

  cdef:
    int result
    uint64_t usec

  result = dbusc.sd_watchdog_enabled(unset_environment, &usec)
  if result < 0:
    raise PystemdDaemonError('Fail to get watchdog information')

  if result > 0:
    return usec

  return 0
