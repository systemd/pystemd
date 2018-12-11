#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

from pystemd.base import SDObject
from pystemd.dbuslib import path_encode
from pystemd.utils import x2char_star


class Unit(SDObject):
    def __init__(self, external_id, bus=None, _autoload=False):
        self.external_id = x2char_star(external_id)
        path = path_encode(b"/org/freedesktop/systemd1/unit", self.external_id)
        super(Unit, self).__init__(
            destination=b"org.freedesktop.systemd1",
            path=path,
            bus=bus,
            _autoload=_autoload,
        )
