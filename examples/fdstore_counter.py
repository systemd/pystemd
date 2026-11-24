#!/usr/bin/env python3
"""
A counter that survives service restarts, kept in a memfd that systemd holds
for the service in its file descriptor store.

    sudo python3 examples/fdstore_counter.py

This script starts itself as a transient Type=notify service (with
FileDescriptorStoreMax=1), restarts it three times, and prints the status each
run reports. Each run reads the count from the memfd, adds one, and writes it
back: the memfd outlives every process, because systemd keeps it between runs
and hands it back through $LISTEN_FDS.
"""

import os
import sys
import time

import pystemd.daemon
import pystemd.run
from pystemd.systemd1 import Unit

UNIT = b"pystemd-fdstore-counter.service"


def service():
    """One run of the service: get the memfd back (or create and store it), count."""
    fds = pystemd.daemon.listen_fds_with_names()
    if "counter" in fds:
        fd = fds["counter"][0]
    else:
        fd = os.memfd_create("counter")
        pystemd.daemon.store_fd("counter", fd)
    count = int(os.pread(fd, 20, 0) or b"0") + 1
    os.pwrite(fd, b"%20d" % count, 0)
    pystemd.daemon.notify(False, ready=1, status=f"run #{count}, pid {os.getpid()}")
    time.sleep(3600)


def wait_for_status(unit, previous):
    """The service's status text, once it's a new one."""
    for _ in range(100):
        status = unit.Service.StatusText.decode()
        if status and status != previous:
            return status
        time.sleep(0.1)
    raise TimeoutError(f"{UNIT.decode()} didn't report a new status")


def main():
    pystemd.run(
        [sys.executable, os.path.abspath(__file__), "--service"],
        name=UNIT,
        service_type="notify",
        extra={b"FileDescriptorStoreMax": 1},
    )
    unit = Unit(UNIT, _autoload=True)
    status = ""
    try:
        for restart in range(4):
            if restart:
                unit.Unit.Restart(b"replace")
            status = wait_for_status(unit, status)
            print(status)
    finally:
        unit.Unit.Stop(b"replace")


if __name__ == "__main__":
    if sys.argv[1:] == ["--service"]:
        service()
    else:
        main()
