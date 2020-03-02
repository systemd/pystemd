#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Any, AnyStr, Dict, Iterable, List, Optional, Tuple

from pystemd.base import SDObject, overwrite_interface_method
from pystemd.dbuslib import DBus, apply_signature
from pystemd.systemd1.unit_signatures import signature_array
from pystemd.unit import SDUnit


class Manager(SDObject):
    def __init__(self, bus: Optional[DBus] = None, _autoload: bool = False) -> None:
        super(Manager, self).__init__(
            destination=b"org.freedesktop.systemd1",
            path=b"/org/freedesktop/systemd1",
            bus=bus,
            _autoload=_autoload,
        )

    @overwrite_interface_method("org.freedesktop.systemd1.Manager")
    def SetUnitProperties(
        self,
        interface_name: bytes,
        unit_name: AnyStr,
        runtime: Any,
        properties: Dict[Any, Any],
    ) -> List[Any]:
        assert interface_name == b"org.freedesktop.systemd1.Manager"
        args = apply_signature(b"sb", [unit_name, runtime])

        args += signature_array(properties)

        with self.bus_context() as bus:
            if bus:
                return bus.call_method(
                    self.destination,
                    self.path,
                    interface_name,
                    b"SetUnitProperties",
                    args,
                ).body
            return []

    @overwrite_interface_method("org.freedesktop.systemd1.Manager")
    def StartTransientUnit(
        self,
        interface_name: bytes,
        name: AnyStr,
        smode: List[Any],
        properties: Dict[Any, Any],
        extra_units: Optional[Iterable[Tuple[bytes, SDUnit]]] = None,
    ) -> List[Any]:
        assert interface_name == b"org.freedesktop.systemd1.Manager"

        args = apply_signature(b"ss", [name, smode])
        args += signature_array(properties)

        # extra units
        args += [(ord(b"a"), b"(sa(sv))")]
        for eu_name, eu_properties in extra_units or []:
            args += [(ord(b"r"), b"sa(sv)")]
            args += apply_signature(b"s", [eu_name])
            args += signature_array(eu_properties)
            args += [(-1, None)]

        args += [(-1, None)]

        with self.bus_context() as bus:
            if bus:
                return bus.call_method(
                    self.destination,
                    self.path,
                    interface_name,
                    b"StartTransientUnit",
                    args,
                ).body
            return []
