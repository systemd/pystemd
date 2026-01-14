"""E2E tests for pystemd Unit functionality"""

import os
import time

import pystemd.run
import pytest


def test_unit_start_stop():
    """Test starting and stopping a transient unit"""
    if os.geteuid() != 0:
        pytest.skip("Requires root privileges")

    # Create a transient unit
    unit = pystemd.run(
        [b"/bin/sleep", b"60"],
        remain_after_exit=True,
    )

    # Wait a moment for it to start
    time.sleep(1)

    # Check it's running
    assert unit.Service.MainPID != 0
    assert unit.Unit.ActiveState == b"active"

    # Stop it
    unit.Unit.Stop(b"replace")

    # Wait for it to stop
    time.sleep(1)
    assert unit.Service.MainPID == 0


def test_unit_restart():
    """Test restarting a unit"""
    if os.geteuid() != 0:
        pytest.skip("Requires root privileges")

    unit = pystemd.run(
        [b"/bin/sleep", b"60"],
        remain_after_exit=True,
    )

    time.sleep(1)
    first_pid = unit.Service.MainPID
    assert first_pid != 0

    # Restart
    unit.Unit.Restart(b"replace")
    time.sleep(1)

    second_pid = unit.Service.MainPID
    assert second_pid != 0
    assert second_pid != first_pid  # Should be different PID

    # Cleanup
    unit.Unit.Stop(b"replace")
