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

from unittest import TestCase
from xml.dom.minidom import parseString as xmlparse

from mock import MagicMock, patch
from pystemd.base import SDObject


class TestContextManager(TestCase):
    def test_context(self):
        with patch.object(SDObject, "load") as load:
            with self.assertRaises(ZeroDivisionError), SDObject(b"d", b"p"):
                raise ZeroDivisionError("we shoudl raise this error")
            load.assert_called_once()


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
        obj._bus.get_property.assert_called_once()

        self.assertIn("meth1", obj.I1.methods)
        obj.I1.meth1(b"arg1")  # just calling a method
        obj._bus.call_method.assert_called_once()

        with self.assertRaises(TypeError):
            obj.I1.meth1()

        with self.assertRaises(TypeError):
            obj.I1.meth1("arg1", "extra args")
