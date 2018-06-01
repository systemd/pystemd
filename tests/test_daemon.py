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

from pystemd import daemon


class TestNotify(TestCase):
    def test_notify(self):
        notify_status = daemon.notify(
            False, "STATUS=one...", b"STATUS=two....", status="last..."
        )
        self.assertIn(notify_status, {0, 1})


class TestListen(TestCase):
    def test_notify(self):
        self.assertTrue(daemon.listen_fds(False) >= 0)

    def test_listen_fds_start(self):
        self.assertEqual(daemon.LISTEN_FDS_START, 3)
