import os
from concurrent.futures import ProcessPoolExecutor
from functools import cached_property
from multiprocessing import Process
from multiprocessing.context import BaseContext
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, cast

import psutil

import pystemd.cutils
import pystemd.run
import pystemd.utils
from pystemd.dbuslib import DBus


class TransientUnitContext(BaseContext):
    """
    Acts as a multiprocessing.context but its systemd unit aware.
    """

    _name = "fork"

    def __init__(
        self,
        properties: Dict[str, Any],
        main_process: Sequence[str] = (),
        user_mode: bool = False,
        unit_name: Optional[str] = None,
    ) -> None:
        self.unit: Optional[pystemd.systemd1.Unit] = None
        self.properties = properties
        self.user_mode = user_mode
        self.unit_name = unit_name 
        self.main_process_cmd = main_process or [
            "/bin/bash",
            "-c",
            "exec sleep infinity",
        ]
        super().__init__()

    def start_unit(self) -> pystemd.systemd1.Unit:
        assert self.unit is None, "Unit already started"
        # pyrefly: ignore [not-callable]
        self.unit = pystemd.run(
            self.main_process_cmd,
            name=self.unit_name,
            user_mode=self.user_mode,
            extra={
                **self.properties,
                "Delegate": True,
            },
        )
        return cast(pystemd.systemd1.Unit, self.unit)

    def stop_unit(self) -> None:
        pystemd.utils.unwrap(self.unit, "unit not started").Unit.Stop(b"replace")

    def Process(self, **kwargs) -> "ProcessFromTransientUnit":
        return ProcessFromTransientUnit(
            **kwargs, unit=pystemd.utils.unwrap(self.unit, "unit not started")
        )


def enter_unit(unit):
    """
    This method is meant to be called when you want the current code to moved to a systemd "unit"
    usually will be called before calling run in a process, and its meant to bootstrap the process
    after fork, but before code to run. It basically do:

        1) Attach itself to the main transient unit (making it part of the cgroup)
        2) Change its namespace too all the namespaces of the main transient unit, this is best effort
        3) Change group and user to the group and user of the main transient unit
    """
    # get the unit information
    main_pid = unit.Service.MainPID

    p = psutil.Process(main_pid)
    uid = p.uids().real
    gid = p.gids().real

    unit.Service.AttachProcesses("/", [os.getpid()])

    # attach ourselves to the namespace
    for ns in Path(f"/proc/{main_pid}/ns").iterdir():
        pystemd.cutils.setns(os.open(ns, os.O_RDONLY), 0)

    # change the user
    os.setgid(gid)
    os.setuid(uid)


class _ProcessWithPreRun(Process):
    """
    Parent class that its just a subprocess, but it execute a pre_run hook
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.original_run = self.run
        self.run = self.pre_run  # type: ignore

    def pre_run(self):
        # pyrefly: ignore [missing-argument]
        self.original_run()


class ProcessFromTransientUnit(_ProcessWithPreRun):
    """
    Given a unit, this class will execute target (or the run method) as if it where part of that unit.
    This class is meant to be use when the systemd unit has already started. Once this process has stop,
    we wont stop the unit.
    """

    def __init__(self, *, unit=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.unit = unit

    def pre_run(self):
        enter_unit(self.unit)
        super().pre_run()


class TransientUnitProcess(_ProcessWithPreRun):
    """
    Given a set of properties, this class will execute target (or the run method) as if it where part of that unit.
    this class will start a unit on its own, and then move the process inside the unit. Then when the process has finish
    the unit will finish.
    """

    def __init__(self, *, properties=None, user_mode=False, unit_name=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.user_mode = user_mode
        self.unit_name = unit_name or pystemd.utils.random_unit_name(prefix="pystemd-future-")  
        self.properties = {
            pystemd.utils.x2char_star(k): v for k, v in (properties or {}).items()
        }

    @cached_property
    def unit(self):
        bus = DBus(user_mode=self.user_mode)
        bus.__enter__()
        return pystemd.systemd1.Unit(self.unit_name, bus, _autoload=True)
    
    def pre_run(self):
        context = TransientUnitContext(
            # pyrefly: ignore [bad-argument-type]
            properties=self.properties,
            user_mode=self.user_mode,
            unit_name=self.unit_name,
            main_process=[
                "/bin/bash",
                "-c",
                f"exec tail --pid={self.pid} -f /dev/null",
            ],
        )
        unit = context.start_unit()
        enter_unit(unit)
        super().pre_run()


class TransientUnitPoolExecutor(ProcessPoolExecutor):
    """
    Same as concurrent.futures.ProcessPoolExecutor but it makes sure the process get
    started in a systemd transient unit
    """

    def __init__(self, properties, user_mode: bool = False, **kwargs):
        self.pool_transient_unit_context = TransientUnitContext(
            properties, user_mode=user_mode
        )
        # pyrefly: ignore [no-matching-overload]
        super().__init__(**{**kwargs, "mp_context": self.pool_transient_unit_context})

    def __enter__(self):
        self.unit = self.pool_transient_unit_context.start_unit()
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            return super().__exit__(exc_type, exc_val, exc_tb)
        finally:
            self.pool_transient_unit_context.stop_unit()


def run(fnc, properties, *args, _user_mode: bool = False, **kwargs):
    """
    Simple helper to call a method in a single worker
    """
    with TransientUnitPoolExecutor(
        properties=properties or {}, max_workers=1, user_mode=_user_mode
    ) as poold:
        future = poold.submit(fnc, *args, **kwargs)
    return future.result()
