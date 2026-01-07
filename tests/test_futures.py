#!/usr/bin/env fbpython
# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

from __future__ import annotations

import os
import unittest
from unittest.mock import MagicMock, Mock, patch

import pystemd.futures


@patch.object(pystemd.futures, "TransientUnitPoolExecutor", autospec=True)
class TestFuturesRun(unittest.TestCase):
    def test_run(self, TransientUnitPoolExecutor: MagicMock) -> None:
        function = Mock()
        properties = Mock()

        result = pystemd.futures.run(function, properties=properties, kwargs="kwarg")
        poold = TransientUnitPoolExecutor.return_value.__enter__.return_value
        self.assertEqual(result, poold.submit.return_value.result.return_value)
        TransientUnitPoolExecutor.assert_called_once_with(
            properties=properties, max_workers=1, user_mode=False
        )
        poold.submit.assert_called_once_with(function, kwargs="kwarg")


@patch.object(pystemd.futures, "TransientUnitContext", autospec=True)
class TestFuturesPool(unittest.TestCase):
    def test_run(self, TransientUnitContext: MagicMock) -> None:
        properties = Mock()
        context = TransientUnitContext.return_value
        with pystemd.futures.TransientUnitPoolExecutor(properties):
            TransientUnitContext.assert_called_once_with(properties, user_mode=False)
            context.start_unit.assert_called_once()
        context.stop_unit.assert_called_once()


@patch("os.setuid", autospec=True)
@patch("os.setgid", autospec=True)
@patch("os.open", autospec=True)
@patch("pystemd.cutils.setns", autospec=True)
@patch.object(pystemd.futures.psutil, "Process", autospec=True)
@patch.object(pystemd.futures, "Path", autospec=True)
class TestEnterUnit(unittest.TestCase):
    def test_enter(
        self,
        Path: MagicMock,
        Process: MagicMock,
        setns: MagicMock,
        os_open: MagicMock,
        os_setgid: MagicMock,
        os_setuid: MagicMock,
    ) -> None:
        unit = Mock()
        main_pid = unit.Service.MainPID
        p = Process.return_value
        uid = p.uids.return_value.real
        gid = p.gids.return_value.real

        pystemd.futures.enter_unit(unit)

        Process.assert_called_once_with(main_pid)
        unit.Service.AttachProcesses.assert_called_once_with("/", [os.getpid()])
        Path.assert_called_once_with(f"/proc/{main_pid}/ns")
        os_setgid.assert_called_once_with(gid)
        os_setuid.assert_called_once_with(uid)


@patch.object(pystemd.futures, "enter_unit", autospec=True)
@patch.object(pystemd.futures, "TransientUnitContext", autospec=True)
@patch("pystemd.utils.random_unit_name", autospec=True, return_value="pystemd-future-test.service")
class TestTransientUnitProcess(unittest.TestCase):
    def test_pre_run(self, random_unit_name: MagicMock, TransientUnitContext: MagicMock, enter_unit: Mock):
        properties = {b"foo": b"bar"}
        target = Mock()
        p = pystemd.futures.TransientUnitProcess(properties=properties, target=target)
        # fake call to per_run
        p.pre_run()
        random_unit_name.assert_called_once_with(prefix="pystemd-future-")
        TransientUnitContext.assert_called_once_with(
            properties=properties,
            user_mode=False,
            unit_name="pystemd-future-test.service",
            main_process=[
                "/bin/bash",
                "-c",
                f"exec tail --pid={p.pid} -f /dev/null",
            ],
        )
        enter_unit.assert_called_once_with(
            TransientUnitContext.return_value.start_unit.return_value
        )
