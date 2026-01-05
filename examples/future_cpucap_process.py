import sys
import time
from contextlib import suppress

import psutil
from psutil import NoSuchProcess

from pystemd.futures import TransientUnitProcess


class Process(TransientUnitProcess):
    def __init__(self, timeout, properties):
        self.timeout = timeout
        super().__init__(properties=properties)

    # pyrefly: ignore [bad-override]
    def run(self):
        """
        This is suppose to waste a bunch of CPU.
        """
        t0 = time.time()
        while time.time() - t0 < self.timeout:
            2**64 - 1


def main(cpu_quota=0.2):
    p = Process(timeout=30, properties={"CPUQuota": cpu_quota, "User": "nobody"})
    p.start()
    process = psutil.Process(p.pid)

    while p.is_alive():
        with suppress(NoSuchProcess):  # the process can die mid check
            cpu_percent = process.cpu_percent(interval=1)
            sys.stdout.write("\033[2J\033[1;1H")
            print(f"current {cpu_percent=}")


if __name__ == "__main__":
    main()
