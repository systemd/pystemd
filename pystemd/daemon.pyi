# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Iterable, Optional, Protocol, Union

class _HasFileno(Protocol):
    def fileno(self) -> int: ...

LISTEN_FDS_START: int

class PystemdDaemonError(Exception):
    pass

def listen_fds(unset_environment: bool) -> int: ...
def notify(
    unset_environment: bool,
    *args: Union[str, bytes],
    fds: Optional[Union[int, _HasFileno, Iterable[Union[int, _HasFileno]]]] = None,
    **kwargs: Union[int, str],
) -> int: ...
def listen_fds_with_names(unset_environment: bool = ...) -> dict[str, list[int]]: ...
def booted() -> bool: ...
def watchdog_enabled(unset_environment: bool) -> int: ...
