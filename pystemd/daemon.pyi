# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Iterable, Mapping, Optional, Protocol, Union

class _HasFileno(Protocol):
    def fileno(self) -> int: ...

_Fds = Union[int, _HasFileno, Iterable[Union[int, _HasFileno]]]

LISTEN_FDS_START: int

class PystemdDaemonError(Exception):
    pass

def listen_fds(unset_environment: bool) -> int: ...
def notify(
    unset_environment: bool,
    *args: Union[str, bytes],
    fds: Optional[_Fds] = None,
    **kwargs: Union[int, str],
) -> int: ...
def listen_fds_with_names(unset_environment: bool = ...) -> dict[str, list[int]]: ...
def store_fd(
    name: str, fds: _Fds, unset_environment: bool = ..., **kwargs: Union[int, str]
) -> int: ...
def store_fds(
    fds_by_name: Mapping[str, _Fds],
    unset_environment: bool = ...,
    **kwargs: Union[int, str],
) -> int: ...
def booted() -> bool: ...
def watchdog_enabled(unset_environment: bool) -> int: ...
