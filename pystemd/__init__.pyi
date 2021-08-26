#
# Copyright (c) 2021-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from pystemd import DBus, __version__, machine1, systemd1

SDUnit = systemd1.Unit
SDManager = systemd1.Manager
SDMachine = machine1.Machine

def run(
    cmd: Any,
    address=...,
    service_type=...,
    name=...,
    user=...,
    user_mode=...,
    nice=...,
    runtime_max_sec=...,
    env=...,
    extra=...,
    cwd=...,
    machine=...,
    wait=False,
    remain_after_exit=False,
    collect=False,
    raise_on_fail=False,
    pty=...,
    pty_master=...,
    pty_path=...,
    stdin=...,
    stdout=...,
    stderr=...,
    _wait_polling=...,
    slice_=...,
): ...
