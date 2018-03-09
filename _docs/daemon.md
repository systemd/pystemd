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
