#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

"""
Linux namespaces helpers.
"""

from __future__ import annotations

import os
from typing import Iterable

# CLONE_NEW* flags, defined here because os only has them from Python 3.12.
# The order is the one nsenter(1) joins them in: user first, mount late.
NAMESPACES = {
    "user": 0x10000000,  # CLONE_NEWUSER
    "cgroup": 0x02000000,  # CLONE_NEWCGROUP
    "ipc": 0x08000000,  # CLONE_NEWIPC
    "uts": 0x04000000,  # CLONE_NEWUTS
    "net": 0x40000000,  # CLONE_NEWNET
    "pid": 0x20000000,  # CLONE_NEWPID
    "mnt": 0x00020000,  # CLONE_NEWNS
    "time": 0x00000080,  # CLONE_NEWTIME
}


def join_namespaces(pid: int, namespaces: Iterable[str] | None = None) -> list[str]:
    """
    Move the calling process into the namespaces of process `pid`, like
    `nsenter --target pid --all`. Returns the names of the namespaces it
    actually joined.

    `namespaces` is an iterable of names (keys of NAMESPACES, e.g.
    ["net", "mnt"]); by default all of them. Namespaces we already share with
    `pid` are skipped (re-joining your own user namespace is an error).

    Joining the pid namespace only affects children created afterwards, the
    calling process keeps its pid. Needs the usual privileges (CAP_SYS_ADMIN,
    or being in a parent user namespace of the target).

    Uses one atomic setns() on a pidfd (Python >= 3.12, Linux >= 5.8) and
    falls back to joining one namespace at a time through /proc/<pid>/ns/*.
    Raises OSError if a namespace can't be joined.
    """
    wanted = list(NAMESPACES) if namespaces is None else list(namespaces)
    if unknown := set(wanted) - set(NAMESPACES):
        raise ValueError(
            f"unknown namespaces {sorted(unknown)}, expected some of {list(NAMESPACES)}"
        )

    to_join = [
        name
        for name in NAMESPACES  # keep nsenter's order
        if name in wanted and _ns_id(pid, name) not in (None, _ns_id("self", name))
    ]
    if not to_join:
        return []

    flags = 0
    for name in to_join:
        flags |= NAMESPACES[name]

    try:
        pidfd = os.pidfd_open(pid)
    except (AttributeError, OSError):  # Linux < 5.3
        pidfd = None
    if pidfd is not None:
        try:
            _setns(pidfd, flags)  # all at once, atomically
            return to_join
        except OSError:  # Linux < 5.8 doesn't take pidfds in setns()
            pass
        finally:
            os.close(pidfd)

    for name in to_join:
        fd = os.open(f"/proc/{pid}/ns/{name}", os.O_RDONLY | os.O_CLOEXEC)
        try:
            _setns(fd, NAMESPACES[name])
        finally:
            os.close(fd)
    return to_join


def _ns_id(pid: int | str, name: str) -> int | None:
    """The inode identifying a namespace, None if the kernel doesn't have it."""
    try:
        return os.stat(f"/proc/{pid}/ns/{name}").st_ino
    except FileNotFoundError:
        return None


def _setns(fd: int, nstype: int) -> None:
    if hasattr(os, "setns"):  # Python >= 3.12
        os.setns(fd, nstype)
        return

    import pystemd.cutils

    if pystemd.cutils.setns(fd, nstype) != 0:
        raise OSError(f"setns(fd={fd}, nstype={nstype:#x}) failed")
