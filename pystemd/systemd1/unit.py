#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pystemd.base import SDObject
from pystemd.dbuslib import path_encode

KNOWN_UNIT_SIGNATURES = {

    b'Slice': b's',
    b'User': b's',
    b'Type': b's',
    b'Group': b's',
    b'Nice': b'i',

    b'Description': b's',
    b'ExecStart': b'a(sasb)',
    b'RemainAfterExit': b'b',

    # stdio signatures
    b'StandardInput': b's',
    b'StandardOutput': b's',
    b'StandardError': b's',
    b'TTYPath': b's',
    b'StandardInputFileDescriptor': b'h',
    b'StandardOutputFileDescriptor': b'h',
    b'StandardErrorFileDescriptor': b'h',
    b'Environment': b'as',

    # timer signatures
    b'OnActiveSec': b't',
    b'RemainAfterElapse': b'b',
    b'OnUnitActiveSec': b't',
    b'OnCalendar': b's',
    b'OnStartupSec': b't',
    b'OnBootSec': b't',
    b'OnUnitInactiveSec': b't',

}


class Unit(SDObject):
    def __init__(self, external_id, bus=None, _autoload=False):
        path = path_encode(
            b'/org/freedesktop/systemd1/unit', external_id)
        super(Unit, self).__init__(
            destination=b'org.freedesktop.systemd1',
            path=path,
            bus=bus,
            _autoload=_autoload)
        self.external_id = external_id
