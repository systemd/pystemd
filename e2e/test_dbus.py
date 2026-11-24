"""E2E tests for D-Bus integration"""

import gc
import os
import select
import time

import pytest

from pystemd.dbusexc import DBusBaseError
from pystemd.dbuslib import DBus


def test_dbus_connection():
    """Test basic D-Bus connection"""
    with DBus() as bus:
        assert bus is not None


def _messages(bus, timeout=5):
    """Yield the messages arriving on `bus` for up to `timeout` seconds."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        msg = bus.process()
        if msg.is_empty():
            select.select([bus.get_fd()], [], [], 0.2)
            continue
        yield msg


def test_reply_has_no_path_interface_or_member():
    """Optional header fields a reply lacks are None (this used to segfault)"""
    with DBus() as bus:
        reply = bus.call_method(
            b"org.freedesktop.systemd1",
            b"/org/freedesktop/systemd1",
            b"org.freedesktop.DBus.Peer",
            b"Ping",
            [],
        )
        assert reply.get_path() is None
        assert reply.get_interface() is None
        assert reply.get_member() is None
        reply.process_reply(True)
        assert reply.headers["Typename"] == "method_return"


def test_message_headers():
    """get_interface() returns the interface (it used to return the path)"""
    if os.geteuid() != 0:
        pytest.skip("BecomeMonitor requires root privileges")

    with DBus() as monitor:
        # only signals: a monitor must never reply, and sd-bus would answer
        # method calls it sees, getting the monitor disconnected
        rule = b"type='signal',sender='org.freedesktop.DBus',member='NameOwnerChanged'"
        monitor.call_method(
            b"org.freedesktop.DBus",
            b"/org/freedesktop/DBus",
            b"org.freedesktop.DBus.Monitoring",
            b"BecomeMonitor",
            [(ord(b"a"), b"s"), (ord(b"s"), rule), (-1, None), (ord(b"u"), 0)],
        )
        with DBus() as other:  # a new connection: NameOwnerChanged for it
            name = other.get_unique_name()

        for msg in _messages(monitor):
            msg.process_reply(False)
            if msg.body[0] == name:
                break
        else:
            pytest.fail("never saw NameOwnerChanged for %r" % name)

        assert msg.get_path() == b"/org/freedesktop/DBus"
        assert msg.get_interface() == b"org.freedesktop.DBus"
        assert msg.get_member() == b"NameOwnerChanged"
        assert msg.get_sender() == b"org.freedesktop.DBus"


def test_close_twice_and_use_after_close():
    """Closing twice is a no-op, using a closed bus raises (it used to abort)"""
    bus = DBus()
    bus.open()
    bus.close()
    bus.close()
    with pytest.raises(DBusBaseError):
        bus.call_method(
            b"org.freedesktop.systemd1",
            b"/org/freedesktop/systemd1",
            b"org.freedesktop.DBus.Peer",
            b"Ping",
            [],
        )
    with pytest.raises(DBusBaseError):
        bus.process()

    # and it can be opened again
    with bus:
        assert bus.get_unique_name().startswith(b":")


def test_match_signal_keeps_callback_alive():
    """sd-bus only borrows the callback: the bus must keep it alive"""
    seen = []

    class Watcher:
        def on_signal(self, msg, error=None, userdata=None):
            msg.process_reply(False)
            seen.append((msg.body, userdata))

    with DBus() as bus:
        # a bound method: it can't take attributes, and nothing else holds it
        bus.match_signal(
            b"org.freedesktop.DBus",
            b"/org/freedesktop/DBus",
            b"org.freedesktop.DBus",
            b"NameOwnerChanged",
            Watcher().on_signal,
            "my-userdata",
        )
        gc.collect()

        with DBus() as other:  # a new connection: NameOwnerChanged for it
            name = other.get_unique_name()

        for _ in _messages(bus):
            if any(body[0] == name for body, _ in seen):
                break
        else:
            pytest.fail("never saw NameOwnerChanged for %r" % name)

    assert all(userdata == "my-userdata" for _, userdata in seen)
