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
    b'DynamicUser': b'b',
    b"Personality": b"s",

    b'Description': b's',
    b'ExecStart': b'a(sasb)',
    b'RemainAfterExit': b'b',

    # stdio signatures
    b'StandardInput': b's',
    b'StandardOutput': b's',
    b'StandardError': b's',
    b'TTYPath': b's',
    b'TTYReset': b'b',
    b'TTYVHangup': b'b',
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

    # paths config
    b'WorkingDirectory': b's',
    b'RootDirectory': b's',
    b'RootImage': b's',

    # binds and paths
    b'BindPaths': b'a(ssbt)',
    b'BindReadOnlyPaths': b'a(ssbt)',
    b"ReadWritePaths": b"as",
    b"ReadOnlyPaths": b"as",
    b"InaccessiblePaths": b"as",
    b"MountFlags": b"t",
    b"PrivateTmp": b"b",
    b"PrivateDevices": b"b",
    b"ProtectKernelTunables": b"b",
    b"ProtectKernelModules": b"b",
    b"ProtectControlGroups": b"b",
    b"PrivateNetwork": b"b",
    b"PrivateUsers": b"b",
    b"ProtectHome": b"s",
    b"ProtectSystem": b"s",

    # Limits
    b"LimitCPU": b"t",
    b"LimitCPUSoft": b"t",
    b"LimitFSIZE": b"t",
    b"LimitFSIZESoft": b"t",
    b"LimitDATA": b"t",
    b"LimitDATASoft": b"t",
    b"LimitSTACK": b"t",
    b"LimitSTACKSoft": b"t",
    b"LimitCORE": b"t",
    b"LimitCORESoft": b"t",
    b"LimitRSS": b"t",
    b"LimitRSSSoft": b"t",
    b"LimitNOFILE": b"t",
    b"LimitNOFILESoft": b"t",
    b"LimitAS": b"t",
    b"LimitASSoft": b"t",
    b"LimitNPROC": b"t",
    b"LimitNPROCSoft": b"t",
    b"LimitMEMLOCK": b"t",
    b"LimitMEMLOCKSoft": b"t",
    b"LimitLOCKS": b"t",
    b"LimitLOCKSSoft": b"t",
    b"LimitSIGPENDING": b"t",
    b"LimitSIGPENDINGSoft": b"t",
    b"LimitMSGQUEUE": b"t",
    b"LimitMSGQUEUESoft": b"t",
    b"LimitNICE": b"t",
    b"LimitNICESoft": b"t",
    b"LimitRTPRIO": b"t",
    b"LimitRTPRIOSoft": b"t",
    b"LimitRTTIME": b"t",
    b"LimitRTTIMESoft": b"t",

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
