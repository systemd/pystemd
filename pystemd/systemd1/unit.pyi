#!/usr/bin/env python3
#
# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Any, AnyStr, Iterator, Optional

from pystemd.base import SDInterface, SDObject
from pystemd.dbuslib import DBus, path_encode
from pystemd.utils import x2char_star

class Unit_Unit(SDInterface):
    def Stop(self, mode): ...
    def LoadState(self): ...
    def ResetFailed(self): ...
    def Restart(self, mode): ...

class Unit_Service(SDInterface):
    MainPID: int
    ExecMainCode: int

class Unit(SDObject):
    def __init__(
        self, external_id: AnyStr, bus: Optional[DBus] = None, _autoload: bool = False
    ): ...
    def __enter__(self) -> Unit: ...
    Unit: Unit_Unit
    Service: Unit_Service
