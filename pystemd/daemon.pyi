# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Union

LISTEN_FDS_START: int

class PystemdDaemonError(Exception):
    pass

def listen_fds(unset_environment: bool) -> int: ...
def notify(unset_environment: bool, *args: Union[str, bytes], **kwargs: Union[int, str]) -> None: ...
def booted() -> bool: ...
def watchdog_enabled(unset_environment: bool) -> int: ...
