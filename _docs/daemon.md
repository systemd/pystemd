# pystemd.daemon

This just provides a python interface to some methods in `sd-daemon.h`, most
important, it provides access to `sd_notify` in a pythonic way (what ever that
means to you). This is built more in the spirit of: if you
already have pystemd installed, why not just use it to `sd_notify` and other
stuff.

Since we are there we also provide 2 other things: access to the listen_fd
passed to your process during socket activation and the starting FD for those
sockets. Just one warning, the `LISTEN_FDS_START` is not really exposed in
`sd-daemon.h` but that has not changed and is probably not going to.

Usage
-----

How to notify? Imagine that this is your service:

```python

import sys
import time
import pystemd.daemon

time.sleep(10) # preparation work
pystemd.daemon.notify(False, ready=1, status="starting to do some work")
for i in range(10):
  time.sleep(1) # some hard work
  pystemd.daemon.notify(False, status=f"Complete: {(i+1)*100}% of work...")

pystemd.daemon.notify(False, 'STOPPING=1')
# this line can also be `pystemd.daemon.notify(False, stopping=1)`

sys.exit(0)

```

and your service unit is

```
[Unit]
Description="my notify example"

[Service]
Type=notify
ExecStart=/usr/bin/python /path/to/my/file.py
```

Then from the moment it starts to the first `pystemd.daemon.notify` your script
is in `activating` state. When you send `pystemd.daemon.notify(False, ready=1)`
you signal systemd that your script is ready and that the service has been
loaded. This also signals systemd that other units that are in the same
transaction and depend on your unit can be started.

`status` calls are meant to provide human readable output on the state of your
service. They are not meant for logging or to store complex structures, but just
to provide feedback for a human querying the state of your service.

The following calls are equivalent: `pystemd.daemon.notify(False, ready=1)` and `pystemd.daemon.notify(False, "READY=1")`

Options of notify can be found in systemd project at: https://github.com/systemd/systemd/blob/master/src/systemd/sd-daemon.h#L173-L232

The first parameter is meant to signal if we should remove the notify
information from the service. For example, you can do
`pystemd.daemon.notify(True, ready=1)`
if you don't intend to speak to the systemd notify socket ever again.


Watchdog
--------

If you set `WatchdogSec=X` in your unit, you can use watchdog functionality. To
get the number of usec between pooling, that is `X*10^6` where `X` is
defined in `WatchdogSec=X`. you can get it with
`pystemd.daemon.watchdog_enabled`, and if you want to ping systemd, you do
`pystemd.daemon.notify(False, watchdog=1)`.


File descriptor store
---------------------

systemd can keep file descriptors for your service while it restarts: a memfd
holding state, a listening socket, even open client connections. The service
hands them over with `sd_notify` (`FDSTORE=1`, the fds attached to the message),
and gets them back on its next start, the same way as socket activation
(`$LISTEN_FDS`, from fd 3, named by `$LISTEN_FDNAMES`). The unit needs
`FileDescriptorStoreMax=` (the number of fds systemd may keep), above 0.

Store fds under a name with `pystemd.daemon.store_fd`, and get them back with
`pystemd.daemon.listen_fds_with_names`, which returns them by name:

```python
import os
import pystemd.daemon

fds = pystemd.daemon.listen_fds_with_names()   # {name: [fd, ...]}
if "state" in fds:
    fd = fds["state"][0]                       # a restart: our memfd is back
else:
    fd = os.memfd_create("state")              # the first run: create it, and store it
    pystemd.daemon.store_fd("state", fd)

pystemd.daemon.notify(False, ready=1)
```

- `store_fd(name, fds, unset_environment=False, **states)` stores one fd or a
  list of them (ints, or objects with `fileno()`); extra states go in the same
  message, e.g. `store_fd("state", fd, ready=1)`.
- `store_fds({name: fds, ...}, unset_environment=False, **states)` stores
  several names, one message per name.
- Both check the names first and raise `ValueError` for an invalid one (1-255
  printable ASCII characters, no `:`): systemd silently ignores a message with
  an invalid `FDNAME=`.
- Underneath, `notify` takes the fds itself: `notify(False, fds=[fd],
  fdstore=1, fdname="state")` is `sd_pid_notify_with_fds()`.
- `listen_fds_with_names` also finds the fds of socket activation by name
  (`FileDescriptorName=` in the socket unit). Names aren't unique, hence the
  lists: a socket unit with several `ListenStream=` passes all its fds under
  one name.

[examples/fdstore_counter.py](../examples/fdstore_counter.py) runs itself as a
service and restarts it a few times: a counter kept in a stored memfd goes up
across the restarts.
