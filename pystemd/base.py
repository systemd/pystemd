#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import re
from contextlib import contextmanager
from xml.dom.minidom import parseString

from pystemd.dbuslib import DBus, apply_signature
from pystemd.utils import x2char_star


class SDObject(object):
    def __init__(self, destination, path, bus=None, _autoload=False):
        self.destination = x2char_star(destination)
        self.path = x2char_star(path)

        self._interfaces = {}
        self._loaded = False
        self._bus = bus

        if _autoload:
            self.load()

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def __getattr__(self, name):
        """
        This methods allow us to call properties and methods from the interfaces
        directly from the SDObject, this way both are equivalents:

            with SDObject(destination, path) as u:
                assert u.Interface.Property1 == u.Property1

        """

        # At some point we should verify that 2 interface do not have the same
        # methods and/or properties. But in the meantime, we can trust that
        # the fine folks at systemd will not do this. they have actually go
        # out of their way to make this true:
        # https://github.com/systemd/systemd/blob/119f0f2876ea340cc41525e844487aa88551c219/src/core/dbus-unit.c#L1738-L1746

        for interface in self._interfaces.values():
            if name in (interface.properties + interface.methods):
                return getattr(interface, name)
        raise AttributeError()

    @contextmanager
    def bus_context(self):
        close_bus_at_end = self._bus is None
        try:
            if self._bus is None:
                bus = DBus()
                bus.open()
            else:
                bus = self._bus
            yield bus
        finally:
            if close_bus_at_end:
                bus.close()

    def get_introspect_xml(self):
        with self.bus_context() as bus:
            xml_doc = parseString(
                bus.call_method(
                    self.destination,
                    self.path,
                    b"org.freedesktop.DBus.Introspectable",
                    b"Introspect",
                    [],
                ).body
            )
            return xml_doc.lastChild

    def load(self, force=False):
        if self._loaded and not force:
            return

        unit_xml = self.get_introspect_xml()
        decoded_destination = self.destination.decode()

        for interface in unit_xml.childNodes:
            if interface.nodeType != interface.ELEMENT_NODE:
                continue

            if interface.tagName != "interface":
                # This is not bad, we just can't act on this info.
                continue

            interface_name = interface.getAttribute("name")

            self._interfaces[interface_name] = meta_interface(interface)(
                self, interface_name
            )

            if interface_name.startswith(decoded_destination):
                setattr(
                    self,
                    interface_name[len(decoded_destination) + 1 :],
                    self._interfaces[interface_name],
                )
            elif interface_name == "org.freedesktop.DBus.Properties":
                self.Properties = self._interfaces[interface_name]


class SDInterface(object):
    def __init__(self, sd_object, interface_name):
        self.sd_object = sd_object
        self.interface_name = x2char_star(interface_name)

    def __repr__(self):
        return "<%s of %s>" % (self.interface_name, self.sd_object.path.decode())

    def _get_property(self, property_name):
        prop_type = self._properties_xml[property_name].getAttribute("type")
        with self.sd_object.bus_context() as bus:
            return bus.get_property(
                self.sd_object.destination,
                self.sd_object.path,
                self.interface_name,
                x2char_star(property_name),
                x2char_star(prop_type),
            )

    def _set_property(self, property_name, value):
        prop_access = self._properties_xml[property_name].getAttribute("access")
        if prop_access == "read":
            raise AttributeError("{} is read-only".format(property_name))
        else:
            raise NotImplementedError("have not implemented set property")

    def _call_method(self, method_name, *args):
        # If the method exist in the sd_object, and it has been authorized to
        # overwrite the method in this interface, call that one
        overwrite_method = getattr(self.sd_object, method_name, None)
        overwrite_interfaces = getattr(overwrite_method, "overwrite_interfaces", [])

        if callable(overwrite_method) and self.interface_name in overwrite_interfaces:
            return overwrite_method(self.interface_name, *args)

        # There is no overwrite in the sd_object, we should call original method
        # we should call the default method (good enough fpor most cases)
        meth = self._methods_xml[method_name]
        in_args = [
            arg.getAttribute("type")
            for arg in meth.childNodes
            if arg.nodeType == arg.ELEMENT_NODE
            and arg.getAttribute("direction") == "in"
        ]

        return self._auto_call_dbus_method(method_name, in_args, *args)

    def _auto_call_dbus_method(self, method_name, in_args, *args):
        if len(args) != len(in_args):
            raise TypeError(
                "method %s require %s arguments, %s supplied"
                % (method_name, len(in_args), len(args))
            )

        block_chars = re.compile(r"v|\{")
        if any(any(block_chars.finditer(arg)) for arg in in_args):
            raise NotImplementedError(
                "still not implemented methods with complex " "arguments"
            )

        in_signature = "".join(in_args)
        call_args = apply_signature(x2char_star(in_signature), list(args))

        with self.sd_object.bus_context() as bus:
            return bus.call_method(
                self.sd_object.destination,
                self.sd_object.path,
                self.interface_name,
                x2char_star(method_name),
                call_args,
            ).body


def _wrap_call_with_name(func, name):
    def _call(self, *args):
        return func(self, name, *args)

    return _call


def extend_class_def(cls, metaclass):
    """extend cls with metaclass"""

    orig_vars = cls.__dict__.copy()
    slots = orig_vars.get("__slots__")
    if slots is not None:
        if isinstance(slots, str):
            slots = [slots]
        for slots_var in slots:
            orig_vars.pop(slots_var)
    orig_vars.pop("__dict__", None)
    orig_vars.pop("__weakref__", None)
    return metaclass(cls.__name__, cls.__bases__, orig_vars)


def meta_interface(interface):
    class _MetaInterface(type):
        def __new__(metacls, classname, baseclasses, attrs):
            attrs.update(
                {
                    "__xml_dom": interface,
                    "properties": [],
                    "methods": [],
                    "_properties_xml": {},
                    "_methods_xml": {},
                }
            )

            _call_method = attrs["_call_method"]
            _get_property = attrs["_get_property"]
            _set_property = attrs["_set_property"]
            elements = [n for n in interface.childNodes if n.nodeType == 1]

            for element in elements:
                if element.tagName == "property":
                    property_name = element.getAttribute("name")

                    attrs["properties"].append(property_name)
                    attrs["_properties_xml"][property_name] = element
                    attrs[property_name] = property(
                        _wrap_call_with_name(_get_property, property_name),
                        _wrap_call_with_name(_set_property, property_name),
                    )

                elif element.tagName == "method":
                    method_name = element.getAttribute("name")
                    attrs["methods"].append(method_name)
                    attrs["_methods_xml"][method_name] = element

                    attrs[method_name] = _wrap_call_with_name(_call_method, method_name)

                    attrs[method_name].__name__ = method_name

            return type.__new__(metacls, classname, baseclasses, attrs)

    return extend_class_def(SDInterface, _MetaInterface)


def overwrite_interface_method(interface):
    "This decorator will sign a method to overwrite a method in a interface"

    def overwrite(func):
        overwrite_interfaces = getattr(func, "overwrite_interfaces", [])
        overwrite_interfaces.append(interface.encode())
        func.overwrite_interfaces = overwrite_interfaces
        return func

    return overwrite
