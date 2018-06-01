#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from itertools import chain
from pprint import pprint

from pystemd.dbuslib import apply_signature, DBus


def monitor(*args):
    """
    This is a simple mock of the monitor function inside busctl. the c version can
    be found in https://github.com/systemd/systemd/blob/master/src/busctl/busctl.c#L1081

    a couple of interesting stuff here:

    1.- We interface directly with dbus, as we need to keep it open.
    2.- we construct argument for `BecomeMonitor`.
    3.- we dump stuff to stdout as simple as possible.
    """

    with DBus() as bus:
        cargs = apply_signature(
            b"asu",  # signature
            [
                chain(
                    *[[b"sender='%s'" % arg, b"destination='%s'" % arg] for arg in args]
                ),
                0,
            ],
        )

        # BecomeMonitor takes 2 argument an array of string (filters) and a
        # uint32 flag. We could have known this by inspecting
        # /org/freedesktop/DBus object.

        bus.call_method(
            b"org.freedesktop.DBus",
            b"/org/freedesktop/DBus",
            b"org.freedesktop.DBus.Monitoring",
            b"BecomeMonitor",
            cargs,
        )

        name = bus.get_unique_name()
        while True:
            msg = bus.process()
            if not msg.is_signal(b"org.freedesktop.DBus", b"NameLost"):
                continue

            msg.process_reply(False)

            if msg.body == name:
                break

        while True:
            msg = bus.process()

            if msg.is_empty():
                bus.wait(1000000000)
                continue

            msg.process_reply(True)
            # print headers
            pprint({k: v for k, v in msg.headers.items() if v is not None})
            # print response
            pprint(msg.body)
            print("#*" * 40)

            if msg.is_signal(b"org.freedesktop.DBus.Local", b"Disconnected"):
                break

            bus.wait(1000000000)
