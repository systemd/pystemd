#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import os
from unittest import TestCase

from pystemd.utils import join_namespaces as reexported
from pystemd.utils.ns import NAMESPACES, join_namespaces


class TestJoinNamespaces(TestCase):
    def test_own_namespaces_is_a_noop(self):
        # we share every namespace with ourselves: nothing to join, no privileges needed
        self.assertEqual(join_namespaces(os.getpid()), [])
        self.assertEqual(join_namespaces(os.getpid(), ["net", "mnt"]), [])

    def test_unknown_namespace(self):
        with self.assertRaises(ValueError):
            join_namespaces(os.getpid(), ["net", "nope"])

    def test_names(self):
        self.assertEqual(
            set(NAMESPACES),
            {"user", "cgroup", "ipc", "uts", "net", "pid", "mnt", "time"},
        )

    def test_reexported(self):
        self.assertIs(reexported, join_namespaces)
