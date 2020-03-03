#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import select
from pprint import pprint

from pystemd.dbuslib import DBus


def process(msg, error=None, userdata=None):
    # read the message True means read Header... usually not needed, we just
    # add it here because this is an example
    msg.process_reply(True)
    print("*" * 80)
    print(" * New message:\n")
    # since we read headers, lets print out the headers
    print("# Mesage headers:")
    pprint({k: v for k, v in msg.headers.items() if v is not None})

    print("\n# Interface:", msg.body[0])
    print("\n# Properties:")
    pprint(msg.body[1])
    print("\n# Data:")
    pprint(msg.body[2])
    print("#" * 80)
    print("\n")


def monitor():

    with DBus() as bus:

        bus.match_signal(
            b"org.freedesktop.systemd1",
            None,
            b"org.freedesktop.DBus.Properties",
            b"PropertiesChanged",
            process,  # callback for this message
            None,
        )
        fd = bus.get_fd()

        while True:
            try:
                select.select([fd], [], [])  # wait for message
                bus.process()  # execute all methods (driver)
            except KeyboardInterrupt:
                break
