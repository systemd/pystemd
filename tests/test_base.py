#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from unittest import TestCase
from unittest.mock import MagicMock, patch
from xml.dom.minidom import parseString as xmlparse

from pystemd.base import SDObject


class TestContextManager(TestCase):
    def test_context(self):
        with patch.object(SDObject, "load") as load:
            with self.assertRaises(ZeroDivisionError), SDObject(b"d", b"p"):
                raise ZeroDivisionError("we shoudl raise this error")
            # Do not use Mock.assert_called_once(), because its not
            # present in python3.5
            self.assertEqual(load.call_count, 1)


class TestLoad(TestCase):
    def setUp(self):
        xml = xmlparse(
            """<node>
            <interface name='non.sysd.interface'></interface>
            <interface name='org.freebeer.obj1.I1'>
                <property name='prop1' type='s'></property>
                <method name='meth1'>
                    <arg direction="in" type="s"/>
                </method>
            </interface>
            </node>"""
        ).firstChild

        self.introspect_path_xml = xml

    def test_set_load(self):
        obj = SDObject(b"org.freebeer.obj1", b"path", bus=MagicMock())
        obj.get_introspect_xml = lambda: self.introspect_path_xml
        obj.load()

        self.assertIn("non.sysd.interface", obj._interfaces)
        self.assertIn("org.freebeer.obj1.I1", obj._interfaces)

        self.assertIn("prop1", obj.I1.properties)
        obj.I1.prop1  # getting a property
        # Do not use Mock.assert_called_once(), because its not
        # present in python3.5
        self.assertEqual(obj._bus.get_property.call_count, 1)

        self.assertIn("meth1", obj.I1.methods)
        obj.I1.meth1(b"arg1")  # just calling a method
        # Do not use Mock.assert_called_once(), because its not
        # present in python3.5
        self.assertEqual(obj._bus.call_method.call_count, 1)

        with self.assertRaises(TypeError):
            obj.I1.meth1()

        with self.assertRaises(TypeError):
            obj.I1.meth1("arg1", "extra args")


class TestGetItem(TestCase):
    def setUp(self):
        super().setUp()

        class FakeInterface:
            def __init__(self):
                self.properties = ["p"]
                self.methods = ["m"]

                self.p = "<fake property>"

            def m(self):
                return "<fake method>"

        self.destination, self.path = b"com.facebook.pystemd", b"/com/facebook/pystemd"
        self.fake_interface = FakeInterface()
        self.sd_obj = SDObject(self.destination, self.path)
        self.sd_obj._interfaces["myinterface"] = self.fake_interface

    def test_find_in_object(self):
        self.assertEqual(self.sd_obj.destination, self.destination)

    def test_find_property_in_interfaces(self):
        self.assertEqual(self.sd_obj.p, self.fake_interface.p)

    def test_find_method_in_interfaces(self):
        self.assertEqual(self.sd_obj.m(), self.fake_interface.m())
