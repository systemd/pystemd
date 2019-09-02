# cython: language_level=3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#


cimport pystemd.dbusc as dbusc

from libc.stdint cimport uint64_t
from pystemd.utils import x2char_star


LISTEN_FDS_START = dbusc.SD_LISTEN_FDS_START

class PystemdDaemonError(Exception):
  "generic daemon error"


def listen_fds(int unset_environment=0):
  return dbusc.sd_listen_fds(unset_environment)


def notify(int unset_environment, *states, **kwstates):
  """
  interface to systemd sd_notify,

  params:
    unset_environment[int] = 1 if we should remove the notify information,
      otherwize 0.
    states/kwstates = array with states statements that are 'IDENTIFIER=VALUE'.
      e.g: 'READY=1' or keywords states like `ready=1`
      (This will be clear in usage).

  usage:
    * `pystemd.daemon.notify(1, ready=1)`: this will signal `READY=1` to systemd
      notify and will remove all information from the environment. You should not
      try to talk to systemd notify socket again.
    *  `pystemd.daemon.notify(True, "READY=1")`: same as above just passed as a
      string.
    *  `pystemd.daemon.notify(False, ready=1, status='gime gime gime')`: will
      signal systemd that the app is ready and also set the status to
      'gime gime gime'. This command does not clean the notify environment.

    For info on sd_notify, check https://github.com/systemd/systemd/blob/\
master/src/systemd/sd-daemon.h#L173-L232

  """
  pystates = [x2char_star(s) for s in states]
  pystates.extend(
    b'='.join([x2char_star(k.upper()), x2char_star(v, convert_all=True)])
    for k, v in kwstates.items()
  )
  state = b'\n'.join(pystates)
  return dbusc.sd_notify(unset_environment, state)


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
