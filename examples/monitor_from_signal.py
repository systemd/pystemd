#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import select  # in python3 you may want to use selector.DefaultSelector
from pprint import pprint

from pystemd.dbuslib import DBus
from pystemd.systemd1 import Unit


class STATE:
    EXIT = False


def process(msg, error=None, userdata=None):
    # read the message True means read Header... usually not needed, we just
    # add it here because this is an example
    msg.process_reply(True)
    print("*" * 80)
    print(" * New message:\n")
    # since we read headers, lets print out the headers
    print("# Message headers:")
    pprint({k: v for k, v in msg.headers.items() if v is not None})

    print("\n# Interface:", msg.body[0])
    print("\n# Properties:")
    pprint(msg.body[1])
    print("\n# Data:")
    pprint(msg.body[2])

    if msg.body[1].get(b"SubState") in (b"exited", b"failed", b"dead"):
        print("Unit is dead, exiting select loop")
        userdata.EXIT = True
    print("#" * 80)
    print("\n")


def monitor(name):

    unit = Unit(name)

    with DBus() as bus:

        bus.match_signal(
            unit.destination,
            unit.path,
            b"org.freedesktop.DBus.Properties",
            b"PropertiesChanged",
            process,  # callback for this message
            STATE,  # maybe pass custom python objects as userdata?
        )
        fd = bus.get_fd()

        while not STATE.EXIT:
            select.select([fd], [], [])  # wait for message
            bus.process()  # execute all methods (driver)
