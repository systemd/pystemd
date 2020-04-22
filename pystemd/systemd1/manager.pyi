#!/usr/bin/env python3
#
# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Any, Dict, List, Optional, Tuple

from pystemd.base import SDInterface, SDObject
from pystemd.dbuslib import DBus

class Manager_Manager(SDInterface):
    def StartTransientUnit(
        self,
        unit_name: bytes,
        mode: bytes,
        properties: Dict[bytes, Any],
        extra_units: Optional[List[Tuple[bytes, Dict[bytes, Any]]]],
    ): ...
    def StartUnit(self, unit_name: bytes, mode: bytes): ...
    def SetUnitProperties(
        self, unit_name: bytes, runtime: bool, properties: Dict[bytes, Any]
    ): ...

class Manager(SDObject):
    def __init__(self, bus: Optional[DBus] = None, _autoload: bool = False): ...
    def __enter__(self) -> Manager: ...
    Manager: Manager_Manager
