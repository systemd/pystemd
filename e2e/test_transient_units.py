"""E2E tests for creating and managing transient units"""

import os
import time

import pytest

import pystemd.run
from pystemd.dbuslib import DBus
from pystemd.systemd1 import Manager, Unit


def test_create_transient_unit_via_manager():
    """Test creating transient unit via Manager API"""
    if os.geteuid() != 0:
        pytest.skip("Requires root privileges")

    unit_name = f"test-{int(time.time())}.service".encode()

    unit_properties = {
        b"Description": b"E2E test transient unit",
        b"ExecStart": [(b"/bin/sleep", (b"/bin/sleep", b"5"), False)],
        b"RemainAfterExit": True,
    }

    with DBus() as bus, Manager(bus=bus) as manager:
        job_path = manager.Manager.StartTransientUnit(
            unit_name, b"fail", unit_properties
        )
        assert job_path is not None

        # Get the unit and check it
        with Unit(unit_name, bus=bus) as unit:
            time.sleep(1)
            assert unit.Service.MainPID != 0
            # Clean up
            unit.Unit.Stop(b"replace")


def test_transient_unit_with_dependencies():
    """Test creating transient unit with dependencies"""
    if os.geteuid() != 0:
        pytest.skip("Requires root privileges")

    unit = pystemd.run(
        [b"/bin/sleep", b"5"],
        extra={
            b"After": [b"network.target"],
        },
        remain_after_exit=True,
    )

    # Check dependencies are set
    assert b"network.target" in unit.Unit.After

    # Cleanup
    unit.Unit.Stop(b"replace")
