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

from pystemd.systemd1 import Manager


def start_transient_unit(cmd="/bin/sleep 15", delay_in_seconds=5):
    a_cmd = [c.encode() for c in shlex.split(cmd)]

    random_unit_name = "myservice.{r}.{t}".format(
        r=random.randint(0, 100), t=time.time()
    )

    timer_unit_name = "{}.timer".format(random_unit_name).encode()
    service_unit_name = "{}.service".format(random_unit_name).encode()

    timer_unit_properties = {
        b"Description": b"Example of transient timer unit",
        b"TimersMonotonic": [(b"OnBootSec", delay_in_seconds * 1000000)],
        b"RemainAfterElapse": False,
    }

    service_unit_properties = {
        b"Description": b"Example of transient unit",
        b"ExecStart": [(a_cmd[0], a_cmd, False)],
        b"RemainAfterExit": True,
    }

    with Manager() as manager:
        manager.Manager.StartTransientUnit(
            timer_unit_name,
            b"fail",
            timer_unit_properties,
            [(service_unit_name, service_unit_properties)],
        )
    print("started {} as timer and service".format(random_unit_name))


if __name__ == "__main__":
    start_transient_unit()
