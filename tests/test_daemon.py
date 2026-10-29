#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import sys
from unittest import TestCase

from pystemd import daemon


class TestNotify(TestCase):
    def test_notify(self):
        notify_status = daemon.notify(
            # pyrefly: ignore [bad-argument-type]
            False,
            "STATUS=one...",
            b"STATUS=two....",
            status="last...",
        )
        self.assertIn(notify_status, {0, 1})

    def test_notify_with_fds(self):
        # without $NOTIFY_SOCKET this is a no-op that returns 0
        with open("/dev/null") as devnull:
            notify_status = daemon.notify(
                # pyrefly: ignore [bad-argument-type]
                False,
                fds=[devnull.fileno(), devnull],
                fdstore=1,
                fdname="test",
            )
        self.assertIn(notify_status, {0, 1})

    def test_notify_with_single_fd(self):
        # a single fd (even 0) is a list of one, not "no fds"
        for fd in (0, 1, sys.stdout):
            # pyrefly: ignore [bad-argument-type]
            self.assertIn(daemon.notify(False, fds=fd, ready=1), {0, 1})

    def test_notify_fds_rejects_non_fds(self):
        for bad in (b"\x03", "abc", [object()], [1.5]):
            with self.assertRaises(TypeError):
                # pyrefly: ignore [bad-argument-type]
                daemon.notify(False, fds=bad, ready=1)


class TestListen(TestCase):
    def test_notify(self):
        self.assertTrue(daemon.listen_fds(False) >= 0)

    def test_listen_fds_with_names(self):
        self.assertIsInstance(daemon.listen_fds_with_names(False), dict)

    def test_listen_fds_start(self):
        self.assertEqual(daemon.LISTEN_FDS_START, 3)
