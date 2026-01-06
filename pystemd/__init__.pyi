#
# Copyright (c) 2021-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Any, Protocol

from pystemd import machine1, systemd1

SDUnit = systemd1.Unit
SDManager = systemd1.Manager
SDMachine = machine1.Machine

class SupportsFileno(Protocol):
    """Protocol for objects that have a fileno() method."""
    def fileno(self) -> int: ...

def run(
    cmd: list[str | bytes] | str | bytes,
    address: str | bytes | None = None,
    service_type: str | bytes | None = None,
    name: str | bytes | None = None,
    user: str | bytes | None = None,
    user_mode: bool = ...,
    nice: int | None = None,
    runtime_max_sec: int | float | None = None,
    env: dict[str | bytes, str | bytes] | None = None,
    extra: dict[bytes, Any] | None = None,
    cwd: str | bytes | None = None,
    machine: str | bytes | None = None,
    wait: bool = False,
    wait_for_activation: bool = False,
    remain_after_exit: bool = False,
    collect: bool = False,
    raise_on_fail: bool = False,
    pty: bool | None = None,
    pty_master: int | None = None,
    pty_path: str | bytes | None = None,
    stdin: int | SupportsFileno | None = None,
    stdout: int | SupportsFileno | None = None,
    stderr: int | SupportsFileno | None = None,
    _wait_polling: int | float | None = None,
    slice_: str | bytes | None = None,
    stop_cmd: list[str | bytes] | str | bytes | None = None,
    stop_post_cmd: list[str | bytes] | str | bytes | None = None,
    start_pre_cmd: list[str | bytes] | str | bytes | None = None,
    start_post_cmd: list[str | bytes] | str | bytes | None = None,
) -> systemd1.Unit: ...
