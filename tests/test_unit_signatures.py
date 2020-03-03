#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from unittest import TestCase

import pystemd.systemd1.unit_signatures


class TestArraySignature(TestCase):
    def test_sample(self):
        self.assertEqual(
            pystemd.systemd1.unit_signatures.signature_array({"PrivateTmp": True}),
            [
                (ord(b"a"), b"(sv)"),
                (ord(b"r"), b"sv"),
                (ord(b"s"), b"PrivateTmp"),
                (ord(b"v"), b"b"),
                (ord(b"b"), True),
                (-1, None),
                (-1, None),
                (-1, None),
            ],
        )
