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

from pystemd.dbuslib import path_encode


class TestEncode(TestCase):
    PREFIX = b"/org/freedesktop/systemd1/unit"
    EXTERNAL_ID = b"s1.service"
    ENCODED_PATH = b"/org/freedesktop/systemd1/unit/s1_2eservice"

    def test_encode(self):
        self.assertEqual(path_encode(self.PREFIX, self.EXTERNAL_ID), self.ENCODED_PATH)

    def test_weird_encode(self):
        self.assertEqual(path_encode(b"/o", self.EXTERNAL_ID), b"/o/s1_2eservice")
