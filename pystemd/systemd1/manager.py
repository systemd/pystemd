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

from pystemd.base import overwrite_interface_method, SDObject
from pystemd.dbuslib import apply_signature
from pystemd.systemd1.unit import KNOWN_UNIT_SIGNATURES
from pystemd.utils import x2char_star


class Manager(SDObject):
    def __init__(self, bus=None, _autoload=False):
        super(Manager, self).__init__(
            destination=b"org.freedesktop.systemd1",
            path=b"/org/freedesktop/systemd1",
            bus=bus,
            _autoload=_autoload,
        )

    @overwrite_interface_method("org.freedesktop.systemd1.Manager")
    def StartTransientUnit(
        self, interface_name, name, smode, properties, extra_units=None
    ):
        assert interface_name == b"org.freedesktop.systemd1.Manager"
        assert extra_units is None, "extra_units not yet supported"

        args = apply_signature(b"ss", [name, smode])
        args += [(ord(b"a"), b"(sv)")]
        for prop_name, prop_value in properties.items():
            prop_name = x2char_star(prop_name)
            signature = KNOWN_UNIT_SIGNATURES[prop_name]

            if callable(signature):
                prop_name, signature, prop_value = signature(prop_name, prop_value)

            args += [(ord(b"r"), b"sv"), (ord(b"s"), prop_name)]
            args += [(ord(b"v"), signature)]
            args += apply_signature(signature, [prop_value])
            args += [(-1, None), (-1, None)]
        args += [(-1, None)]

        # extra units
        args += [(ord(b"a"), b"(sa(sv))")]
        args += [(-1, None)]

        with self.bus_context() as bus:
            return bus.call_method(
                self.destination, self.path, interface_name, b"StartTransientUnit", args
            ).body
