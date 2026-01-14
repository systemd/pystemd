"""E2E tests for pystemd.run functionality"""

import os
import time

import pystemd.run
import pytest
from pystemd.exceptions import PystemdRunError


def test_simple_command():
    """Test running a simple command"""
    unit = pystemd.run([b"/bin/true"], remain_after_exit=True)
    assert unit is not None
    assert unit.Service.ExecMainStatus == 0


def test_command_with_args():
    """Test running command with arguments"""
    unit = pystemd.run([b"/bin/sleep", b"1"], remain_after_exit=True, wait=True)
    assert unit is not None
    assert unit.Service.MainPID == 0  # Should have exited
    assert unit.Service.ExecMainStatus == 0


def test_command_with_env():
    """Test running command with environment variables"""
    unit = pystemd.run(
        [b"/bin/sh", b"-c", b'test "$MY_VAR" = "test_value"'],
        env={b"MY_VAR": b"test_value"},
        remain_after_exit=True,
        wait=True,
    )
    assert unit.Service.ExecMainStatus == 0


def test_command_with_cwd():
    """Test running command with custom working directory"""
    unit = pystemd.run(
        [b"/bin/pwd"],
        cwd=b"/tmp",
        remain_after_exit=True,
        wait=True,
    )
    assert unit.Service.ExecMainStatus == 0


def test_command_with_user():
    """Test running command as different user (requires root)"""
    if os.geteuid() != 0:
        pytest.skip("Requires root privileges")

    unit = pystemd.run(
        [b"/bin/id", b"-u"],
        user=b"nobody",
        remain_after_exit=True,
        wait=True,
    )
    assert unit.Service.ExecMainStatus == 0


def test_wait_for_activation():
    """Test wait_for_activation parameter"""
    unit = pystemd.run(
        [b"/bin/sleep", b"10"],
        wait_for_activation=True,
        remain_after_exit=True,
    )
    # Should return quickly after activation
    assert unit.Service.MainPID != 0  # Still running
    # Clean up
    unit.Unit.Stop(b"replace")


def test_raise_on_fail():
    """Test raise_on_fail parameter"""
    with pytest.raises(PystemdRunError):
        pystemd.run(
            [b"/bin/false"],
            wait=True,
            raise_on_fail=True,
        )


def test_runtime_max_sec():
    """Test runtime_max_sec timeout"""
    start = time.time()
    unit = pystemd.run(
        [b"/bin/sleep", b"100"],
        runtime_max_sec=2,
        remain_after_exit=True,
        wait=True,
    )
    elapsed = time.time() - start
    # Should have been killed after ~2 seconds
    assert elapsed < 10
    assert unit.Service.ExecMainStatus != 0  # Should have non-zero exit


def test_service_type_oneshot():
    """Test service_type parameter"""
    unit = pystemd.run(
        [b"/bin/true"],
        service_type=b"oneshot",
        remain_after_exit=True,
        wait=True,
    )
    assert unit.Service.ExecMainStatus == 0


def test_stop_cmd():
    """Test stop_cmd parameter"""
    unit = pystemd.run(
        [b"/bin/sleep", b"100"],
        stop_cmd=[b"/bin/echo", b"stopping"],
        remain_after_exit=True,
    )
    # Give it a moment to start
    time.sleep(1)
    assert unit.Service.MainPID != 0
    # Stop it
    unit.Unit.Stop(b"replace")
    time.sleep(1)
    assert unit.Service.MainPID == 0
