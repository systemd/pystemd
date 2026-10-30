#!/usr/bin/env fbpython
# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

import pystemd.run

# pystemd.run is the function; the module it was defined in is kept here
run_module = pystemd.run.__module__


@patch.object(run_module, "Unit", autospec=True)
@patch.object(run_module, "SDManager")
@patch.object(run_module, "DBus")
class TestRunDelegate(unittest.TestCase):
    def unit_properties(self, SDManager: MagicMock, **kwargs: object) -> dict:
        run_module.run(["/bin/true"], user_mode=False, **kwargs)
        manager = SDManager.return_value.__enter__.return_value
        (_name, _mode, properties), _ = manager.Manager.StartTransientUnit.call_args
        return properties

    def test_delegate_default_is_not_sent(self, DBus, SDManager, Unit) -> None:
        self.assertNotIn(b"Delegate", self.unit_properties(SDManager))

    def test_delegate_true(self, DBus, SDManager, Unit) -> None:
        self.assertIs(self.unit_properties(SDManager, delegate=True)[b"Delegate"], True)

    def test_delegate_false(self, DBus, SDManager, Unit) -> None:
        self.assertIs(
            self.unit_properties(SDManager, delegate=False)[b"Delegate"], False
        )

    def test_extra_still_wins(self, DBus, SDManager, Unit) -> None:
        properties = self.unit_properties(
            SDManager, delegate=True, extra={b"Delegate": False}
        )
        self.assertIs(properties[b"Delegate"], False)
