"""E2E tests for D-Bus integration"""

from pystemd.dbuslib import DBus
from pystemd.systemd1 import Manager


def test_dbus_connection():
    """Test basic D-Bus connection"""
    with DBus() as bus:
        assert bus is not None


# def test_dbus_user_mode():
#     """Test user-mode D-Bus connection"""
#     with DBus(user_mode=True) as bus:
#         assert bus is not None
#         # Should be able to connect to user bus
#         with Manager(bus=bus) as manager:
#             version = manager.Manager.Version
#             assert version is not None
