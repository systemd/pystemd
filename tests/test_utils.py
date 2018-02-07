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

import six
from unittest import TestCase

from pystemd.utils import x2char_star


class TestContextToCharStar(TestCase):
    def test_pass_normal_vars(self):
        for elem in (0, six.b('hi'), True, [], {}, (3, 4), {3, 4}):
            self.assertEqual(elem, x2char_star(elem))

    def test_convert_to_char(self):
        for elem in ("", u'hi all'):
            self.assertEqual(six.b(elem), x2char_star(elem))
