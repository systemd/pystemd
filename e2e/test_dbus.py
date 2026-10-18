"""E2E tests for D-Bus integration"""

import os

import pytest

from pystemd.dbuslib import DBus


def test_dbus_connection():
    """Test basic D-Bus connection"""
    with DBus() as bus:
        assert bus is not None


def test_failed_call_does_not_leak():
    """A failed method call must release its message, including passed fds"""
    fd = os.open("/dev/null", os.O_RDONLY)
    try:
        with DBus() as bus:

            def fail():
                with pytest.raises(Exception, match="NoSuchMethod"):
                    bus.call_method(
                        b"org.freedesktop.DBus",
                        b"/org/freedesktop/DBus",
                        b"org.freedesktop.DBus",
                        b"NoSuchMethod",
                        [(ord(b"h"), fd)],
                    )

            fail()
            before = len(os.listdir("/proc/self/fd"))
            for _ in range(100):
                fail()
            assert len(os.listdir("/proc/self/fd")) == before
    finally:
        os.close(fd)
