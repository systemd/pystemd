#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

from pystemd.base import SDObject, overwrite_interface_method
from pystemd.dbuslib import apply_signature
from pystemd.systemd1.unit_signatures import signature_array


class Manager(SDObject):
    def __init__(self, bus=None, _autoload=False):
        super(Manager, self).__init__(
            destination=b"org.freedesktop.systemd1",
            path=b"/org/freedesktop/systemd1",
            bus=bus,
            _autoload=_autoload,
        )

    @overwrite_interface_method("org.freedesktop.systemd1.Manager")
    def SetUnitProperties(self, interface_name, unit_name, runtime, properties):
        assert interface_name == b"org.freedesktop.systemd1.Manager"
        args = apply_signature(b"sb", [unit_name, runtime])

        args += signature_array(properties)

        with self.bus_context() as bus:
            return bus.call_method(
                self.destination, self.path, interface_name, b"SetUnitProperties", args
            ).body

    @overwrite_interface_method("org.freedesktop.systemd1.Manager")
    def StartTransientUnit(
        self, interface_name, name, smode, properties, extra_units=None
    ):
        assert interface_name == b"org.freedesktop.systemd1.Manager"
        assert extra_units is None, "extra_units not yet supported"

        args = apply_signature(b"ss", [name, smode])
        args += signature_array(properties)

        # extra units
        args += [(ord(b"a"), b"(sa(sv))")]
        args += [(-1, None)]

        with self.bus_context() as bus:
            return bus.call_method(
                self.destination, self.path, interface_name, b"StartTransientUnit", args
            ).body
