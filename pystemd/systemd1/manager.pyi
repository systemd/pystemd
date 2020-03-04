#!/usr/bin/env python3
#
# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Optional

from pystemd.base import SDInterface, SDObject
from pystemd.dbuslib import DBus

class Manager_Manager(SDInterface):
    def StartUnit(self, unit_name, mode): ...

class Manager(SDObject):
    def __init__(self, bus: Optional[DBus] = None, _autoload: bool = False): ...
    def __enter__(self) -> Manager: ...
    Manager: Manager_Manager
