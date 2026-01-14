import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from threading import Thread

import psutil
from psutil import NoSuchProcess
from pystemd.futures import TransientUnitPoolExecutor


def run(timeout):
    """
    This methods just uses a lot of CPU
    """
    t0 = time.time()
    while time.time() - t0 < timeout:
        2**64 - 1

    return timeout


class MyTop(Thread):
    """
    This class just shows a top like cpu ussage of the processes
    """

    def __init__(self, unit):
        self.unit = unit
        super().__init__()

    def run(self):
        time.sleep(1)
        with ThreadPoolExecutor() as tpool, suppress(NoSuchProcess):
            all_process = self.unit.Service.GetProcesses()

            while self.unit.Unit.ActiveState != b"inactive":
                sys.stdout.write("\033[2J\033[1;1H")
                for cpu, (_, pid, cmd) in zip(
                    tpool.map(
                        lambda pid: psutil.Process(pid).cpu_percent(interval=0.5),
                        [pid for _, pid, __ in all_process],
                    ),
                    all_process,
                ):
                    print(pid, cmd.decode(), cpu)


def main(cpu_quota=0.25):
    with TransientUnitPoolExecutor(
        properties={"CPUQuota": cpu_quota, "User": "nobody"},
        max_workers=10,
        user_mode=os.getuid() != 0,
    ) as poold:
        top = MyTop(poold.unit)
        top.start()

        poold.submit(run, 5)
        poold.submit(run, 10)
        poold.submit(run, 15)
        poold.submit(run, 20)
        poold.submit(run, 25)
        poold.submit(run, 30)


if __name__ == "__main__":
    main()
