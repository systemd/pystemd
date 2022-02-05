#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import random
import shlex
import time

from pystemd.dbuslib import DBus
from pystemd.systemd1 import Manager, Unit


def start_transient_unit(cmd="/bin/sleep 15"):
    a_cmd = [c.encode() for c in shlex.split(cmd)]
    random_unit_name = "myservice.{r}.{t}.service".format(
        r=random.randint(0, 100), t=time.time()
    ).encode()

    unit = {
        b"Description": b"Example of transient unit",
        b"ExecStart": [(a_cmd[0], a_cmd, False)],
        b"RemainAfterExit": True,
    }
    # if we need interactive prompts for passwords, we can create our own DBus object.
    # if we dont need interactive, we would just do `with Manager() as manager:`.
    with DBus(interactive=True) as bus, Manager(bus=bus) as manager:
        manager.Manager.StartTransientUnit(random_unit_name, b"fail", unit)

        with Unit(random_unit_name, bus=bus) as unit:
            while True:
                print(
                    "service `{cmd}` (name={random_unit_name}) has MainPID "
                    "{unit.Service.MainPID}".format(**locals())
                )
                if unit.Service.MainPID == 0:
                    print(
                        "service finished with "
                        "{unit.Service.ExecMainStatus}/{unit.Service.Result} "
                        "will stop it and then... bye".format(**locals())
                    )
                    unit.Unit.Stop(b"replace")
                    break
                print("service still running, sleeping by 5 seconds")
                time.sleep(5)
