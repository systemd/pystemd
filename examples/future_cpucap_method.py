import time

from pystemd import futures


def run(timeout):
    """
    This methods just uses a lot of CPU
    """
    t0 = time.time()
    while time.time() - t0 < timeout:
        2**64 - 1

    return timeout


def main(cpu_quota=0.2, timeout=15):
    return futures.run(run, {"CPUQuota": cpu_quota, "User": "nobody"}, timeout=timeout)


if __name__ == "__main__":
    print(f"result is {main()=}")
