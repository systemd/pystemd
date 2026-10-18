#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import subprocess
import sys
from pathlib import Path
from unittest import TestCase

import pystemd.systemd1.unit_signatures
from pystemd.systemd1.transient_properties import TRANSIENT_PROPERTY_SIGNATURES
from pystemd.systemd1.unit_signatures import CONVENIENCE_PROPERTIES


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

    def test_set_signature_differs_from_read_type(self):
        # ExecStart is read as a(sasbttttuii) but set as a(sasb).
        args = pystemd.systemd1.unit_signatures.signature_array(
            {b"ExecStart": [(b"/bin/true", [b"/bin/true"], False)]}
        )
        self.assertIn((ord(b"v"), b"a(sasb)"), args)

    def test_unknown_property(self):
        with self.assertRaises(KeyError):
            pystemd.systemd1.unit_signatures.signature_array({b"NoSuchProperty": 1})


class TestConvenienceProperties(TestCase):
    def test_targets_are_transient_properties(self):
        """Every convenience must send a property systemd accepts, with the
        signature systemd accepts it with."""
        for name, convert in CONVENIENCE_PROPERTIES.items():
            if name == b"_custom":
                continue
            with self.subTest(name=name):
                target, signature, _ = convert(name, 1)
                self.assertEqual(TRANSIENT_PROPERTY_SIGNATURES[target], signature)

    def test_do_not_shadow_transient_properties(self):
        self.assertFalse(
            set(CONVENIENCE_PROPERTIES) & set(TRANSIENT_PROPERTY_SIGNATURES)
        )


class TestGeneratedModule(TestCase):
    def test_up_to_date(self):
        tool = Path(__file__).parent.parent / "tools/generate_transient_properties.py"
        subprocess.run([sys.executable, str(tool), "--check"], check=True)
