#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import AnyStr, Optional

from pystemd.base import SDObject
from pystemd.dbuslib import DBus, path_encode
from pystemd.utils import x2char_star


class Unit(SDObject):
    external_id: bytes

    def __init__(
        self, external_id: AnyStr, bus: Optional[DBus] = None, _autoload: bool = False
    ) -> None:
        maybebytes = x2char_star(external_id)
        if isinstance(maybebytes, bytes):
            self.external_id = maybebytes
        else:
            self.external_id = b""
        path = path_encode(b"/org/freedesktop/systemd1/unit", self.external_id)
        super(Unit, self).__init__(
            destination=b"org.freedesktop.systemd1",
            path=path,
            bus=bus,
            _autoload=_autoload,
        )
