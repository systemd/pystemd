#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import pathlib
from unittest import TestCase

from pystemd.utils import x2char_star


class TestContextToCharStar(TestCase):
    def test_pass_normal_vars(self):
        for elem in (0, b"hi", True, [], {}, (3, 4), {3, 4}):
            self.assertEqual(elem, x2char_star(elem))

    def test_convert_to_char(self):
        for elem in ("", "hi all"):
            self.assertEqual(elem.encode(), x2char_star(elem))

        self.assertEqual(b"/this/is/path", x2char_star(pathlib.Path("/this/is/path")))

    def test_convert_all(self):
        self.assertEqual(b"true", x2char_star(True, convert_all=True))
        self.assertEqual(b"false", x2char_star(False, convert_all=True))
        self.assertEqual(b"1", x2char_star(1, convert_all=True))
        self.assertEqual(b"3.14159", x2char_star(3.14159, convert_all=True))
        self.assertEqual(b"100", x2char_star(100, convert_all=True))
