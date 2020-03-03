#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.


import random
import shlex
import textwrap
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


def start_webserver(listen_stream="0.0.0.0:7042",):
    a_cmd = [
        "/usr/bin/python3",
        "-c",
        textwrap.dedent(
            """
            import socket

            with socket.fromfd(3, socket.AF_INET, socket.SOCK_STREAM) as s:
                conn, addr = s.accept()
                with conn:
                    print(f"got connection from {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data: break
                        print(data)
                        conn.sendall(data)
            """
        ),
    ]

    random_unit_name = "myservice.{r}.{t}".format(
        r=random.randint(0, 100), t=time.time()
    )

    socket_unit_name = "{}.socket".format(random_unit_name).encode()
    service_unit_name = "{}.service".format(random_unit_name).encode()

    socket_unit_properties = {
        b"Description": b"Example of transient socket unit",
        b"Listen": [("Stream", listen_stream)],
    }

    service_unit_properties = {
        b"Description": b"Example of transient unit",
        b"ExecStart": [(a_cmd[0], a_cmd, False)],
        b"RemainAfterExit": True,
    }

    with Manager() as manager:
        manager.Manager.StartTransientUnit(
            socket_unit_name,
            b"fail",
            socket_unit_properties,
            [(service_unit_name, service_unit_properties)],
        )
    print("started {} as socket and service".format(random_unit_name))


if __name__ == "__main__":
    start_transient_unit()
