#!/usr/bin/env python3
#
# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from unittest import TestCase
from unittest.mock import ANY, call, patch

import pystemd.journal
from pystemd.utils import x2char_star


class TestJournalLog(TestCase):
    MESSAGE = "my message"
    PRIORITY = 101

    @patch("pystemd.journal.sendv")
    def test_msg(self, sendv):

        pystemd.journal.log(self.PRIORITY, self.MESSAGE)
        LOG_LINE = 24
        # ^^ that should be the line we called pystemd.journal.log.

        self.assertEqual(sendv.call_count, 1, "sendv should only be called once")

        sendv.call_args.assert_called_with(
            call(
                CODE_CONTEXT=ANY,
                CODE_LINE=LOG_LINE,
                CODE_FILE=__file__,
                MESSAGE=x2char_star(self.MESSAGE),
                PRIORITY=self.PRIORITY,
                CODE_FUNC="test_msg",
            )
        )
