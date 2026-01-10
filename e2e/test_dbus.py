"""E2E tests for D-Bus integration"""

from pystemd.dbuslib import DBus


def test_dbus_connection():
    """Test basic D-Bus connection"""
    with DBus() as bus:
        assert bus is not None
