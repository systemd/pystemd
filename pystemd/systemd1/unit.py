#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from __future__ import annotations

from pystemd.base import SDObject, overwrite_interface_method
from pystemd.dbuslib import apply_signature, path_encode
from pystemd.systemd1.unit_signatures import signature_array
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

    # pyrefly: ignore [bad-override]
    def __getstate__(self):
        return {
            "external_id": self.external_id,
            "bus": self._bus,
            "_autoload": self._loaded,
        }

    @overwrite_interface_method("org.freedesktop.systemd1.Unit")
    def SetProperties(self, interface_name, runtime, properties):
        """
        Change unit properties at runtime, like `systemctl set-property`.
        `properties` is a dict (or a list of (name, value) pairs), e.g.
        `unit.Unit.SetProperties(True, {"CPUWeight": 200})`; each value is
        sent with the type systemd expects for it (see KNOWN_UNIT_SIGNATURES).
        """
        assert interface_name == b"org.freedesktop.systemd1.Unit"
        args = apply_signature(b"b", [runtime])
        args += signature_array(properties)

        with self.bus_context() as bus:
            return bus.call_method(
                self.destination, self.path, interface_name, b"SetProperties", args
            ).body
