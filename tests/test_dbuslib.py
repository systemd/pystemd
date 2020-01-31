#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import errno
import pathlib
import socket
import tempfile
from unittest import TestCase

from pystemd.dbusexc import DBusConnectionRefusedError, DBusFileNotFoundError
from pystemd.dbuslib import DBusAddress, path_decode, path_encode


class TestEncode(TestCase):
    PREFIX = b"/org/freedesktop/systemd1/unit"
    EXTERNAL_ID = b"s1.service"
    ENCODED_PATH = b"/org/freedesktop/systemd1/unit/s1_2eservice"

    def test_encode(self):
        self.assertEqual(path_encode(self.PREFIX, self.EXTERNAL_ID), self.ENCODED_PATH)

    def test_weird_encode(self):
        self.assertEqual(path_encode(b"/o", self.EXTERNAL_ID), b"/o/s1_2eservice")

    def test_decode(self):
        self.assertEqual(path_decode(self.ENCODED_PATH, self.PREFIX), self.EXTERNAL_ID)

    def test_weird_decode(self):
        self.assertEqual(path_decode(b"/o/s1_2eservice", b"/o"), self.EXTERNAL_ID)


class TestDBusError(TestCase):
    def test_connecting_to_serverless_socket_raises_connection_refused_error(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            socket_path = pathlib.Path(temporary_directory) / "test_socket"
            with socket.socket(
                family=socket.AF_UNIX, type=socket.SOCK_STREAM
            ) as server:
                server.bind(bytes(socket_path))

                dbus = DBusAddress(self.dbus_address_from_unix_socket_path(socket_path))
                with self.assertRaises(DBusConnectionRefusedError) as expectation:
                    dbus.open()
                self.assertEqual(expectation.exception.errno, -errno.ECONNREFUSED)

    def test_connecting_to_missing_socket_raises_file_not_found_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            socket_path = pathlib.Path(temporary_directory) / "test_socket"
            dbus = DBusAddress(self.dbus_address_from_unix_socket_path(socket_path))
            with self.assertRaises(DBusFileNotFoundError) as expectation:
                dbus.open()
            self.assertEqual(expectation.exception.errno, -errno.ENOENT)

    @staticmethod
    def dbus_address_from_unix_socket_path(socket_path: pathlib.Path) -> bytes:
        return b"unix:path=" + bytes(socket_path)
