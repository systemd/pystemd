#
# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Any, Dict, List, Optional, Tuple

from pystemd.base import SDInterface, SDObject
from pystemd.dbuslib import DBus

UnitFileChange = Tuple[
    bytes,  # Type of the change (one of symlink or unlink)
    bytes,  # File name of the symlink
    bytes,  # Destination of the symlink
]

class Manager_Manager(SDInterface):
    def StartTransientUnit(
        self,
        unit_name: bytes,
        mode: bytes,
        properties: Dict[bytes, Any],
        extra_units: Optional[List[Tuple[bytes, Dict[bytes, Any]]]],
    ): ...
    def StartUnit(self, unit_name: bytes, mode: bytes): ...
    def StopUnit(self, unit_name: bytes, mode: bytes): ...
    def SetUnitProperties(
        self, unit_name: bytes, runtime: bool, properties: Dict[bytes, Any]
    ): ...
    def EnableUnitFiles(
        self, units: List[bytes], runtime: bool, force: bool
    ) -> Tuple[bool, List[UnitFileChange]]: ...
    def DisableUnitFiles(
        self, units: List[bytes], runtime: bool
    ) -> List[UnitFileChange]: ...
    # autogenerated
    def GetUnit(self, arg0: bytes) -> bytes: ...  # s  # o
    def GetUnitByPID(self, arg0: int) -> bytes: ...  # u  # o
    def GetUnitByInvocationID(self, arg0: List[int]) -> bytes: ...  # ay  # o
    def GetUnitByControlGroup(self, arg0: bytes) -> bytes: ...  # s  # o
    def LoadUnit(self, arg0: bytes) -> bytes: ...  # s  # o
    def StartUnitReplace(
        self, arg0: bytes, arg1: bytes, arg2: bytes  # s  # s  # s
    ) -> bytes: ...  # o
    def ReloadUnit(self, arg0: bytes, arg1: bytes) -> bytes: ...  # s  # s  # o
    def RestartUnit(self, arg0: bytes, arg1: bytes) -> bytes: ...  # s  # s  # o
    def TryRestartUnit(self, arg0: bytes, arg1: bytes) -> bytes: ...  # s  # s  # o
    def ReloadOrRestartUnit(self, arg0: bytes, arg1: bytes) -> bytes: ...  # s  # s  # o
    def ReloadOrTryRestartUnit(
        self, arg0: bytes, arg1: bytes  # s  # s
    ) -> bytes: ...  # o
    def EnqueueUnitJob(
        self, arg0: bytes, arg1: bytes, arg2: bytes  # s  # s  # s
    ) -> Tuple[
        int, bytes, bytes, bytes, bytes, List[Tuple[int, bytes, bytes, bytes, bytes]]
    ]: ...  # (uososa(uosos))
    def KillUnit(self, arg0: bytes, arg1: bytes, arg2: int) -> None: ...  # s  # s  # i
    def CleanUnit(self, arg0: bytes, arg1: List[bytes]) -> None: ...  # s  # as
    def ResetFailedUnit(self, arg0: bytes) -> None: ...  # s
    def RefUnit(self, arg0: bytes) -> None: ...  # s
    def UnrefUnit(self, arg0: bytes) -> None: ...  # s
    def GetUnitProcesses(
        self, arg0: bytes  # s
    ) -> List[Tuple[bytes, int, bytes]]: ...  # a(sus)
    def AttachProcessesToUnit(
        self, arg0: bytes, arg1: bytes, arg2: List[int]  # s  # s  # au
    ) -> None: ...
    def AbandonScope(self, arg0: bytes) -> None: ...  # s
    def GetJob(self, arg0: int) -> bytes: ...  # u  # o
    def GetJobAfter(
        self, arg0: int  # u
    ) -> List[Tuple[int, bytes, bytes, bytes, bytes, bytes]]: ...  # a(usssoo)
    def GetJobBefore(
        self, arg0: int  # u
    ) -> List[Tuple[int, bytes, bytes, bytes, bytes, bytes]]: ...  # a(usssoo)
    def CancelJob(self, arg0: int) -> None: ...  # u
    def ClearJobs(self) -> None: ...
    def ResetFailed(self) -> None: ...
    def ListUnits(
        self,
    ) -> List[
        Tuple[bytes, bytes, bytes, bytes, bytes, bytes, bytes, int, bytes, bytes]
    ]: ...  # a(ssssssouso)
    def ListUnitsFiltered(
        self, arg0: List[bytes]  # as
    ) -> List[
        Tuple[bytes, bytes, bytes, bytes, bytes, bytes, bytes, int, bytes, bytes]
    ]: ...  # a(ssssssouso)
    def ListUnitsByPatterns(
        self, arg0: List[bytes], arg1: List[bytes]  # as  # as
    ) -> List[
        Tuple[bytes, bytes, bytes, bytes, bytes, bytes, bytes, int, bytes, bytes]
    ]: ...  # a(ssssssouso)
    def ListUnitsByNames(
        self, arg0: List[bytes]  # as
    ) -> List[
        Tuple[bytes, bytes, bytes, bytes, bytes, bytes, bytes, int, bytes, bytes]
    ]: ...  # a(ssssssouso)
    def ListJobs(
        self,
    ) -> List[Tuple[int, bytes, bytes, bytes, bytes, bytes]]: ...  # a(usssoo)
    def Subscribe(self) -> None: ...
    def Unsubscribe(self) -> None: ...
    def Dump(self) -> bytes: ...  # s
    def DumpByFileDescriptor(self) -> int: ...  # h
    def Reload(self) -> None: ...
    def Reexecute(self) -> None: ...
    def Exit(self) -> None: ...
    def Reboot(self) -> None: ...
    def PowerOff(self) -> None: ...
    def Halt(self) -> None: ...
    def KExec(self) -> None: ...
    def SwitchRoot(self, arg0: bytes, arg1: bytes) -> None: ...  # s  # s
    def SetEnvironment(self, arg0: List[bytes]) -> None: ...  # as
    def UnsetEnvironment(self, arg0: List[bytes]) -> None: ...  # as
    def UnsetAndSetEnvironment(
        self, arg0: List[bytes], arg1: List[bytes]  # as  # as
    ) -> None: ...
    def ListUnitFiles(self) -> List[Tuple[bytes, bytes]]: ...  # a(ss)
    def ListUnitFilesByPatterns(
        self, arg0: List[bytes], arg1: List[bytes]  # as  # as
    ) -> List[Tuple[bytes, bytes]]: ...  # a(ss)
    def GetUnitFileState(self, arg0: bytes) -> bytes: ...  # s  # s
    def ReenableUnitFiles(
        self, arg0: List[bytes], arg1: bool, arg2: bool  # as  # b  # b
    ) -> Tuple[bool, List[Tuple[bytes, bytes, bytes]]]: ...  # (ba(sss))
    def LinkUnitFiles(
        self, arg0: List[bytes], arg1: bool, arg2: bool  # as  # b  # b
    ) -> List[Tuple[bytes, bytes, bytes]]: ...  # a(sss)
    def PresetUnitFiles(
        self, arg0: List[bytes], arg1: bool, arg2: bool  # as  # b  # b
    ) -> Tuple[bool, List[Tuple[bytes, bytes, bytes]]]: ...  # (ba(sss))
    def PresetUnitFilesWithMode(
        self,
        arg0: List[bytes],  # as
        arg1: bytes,  # s
        arg2: bool,  # b
        arg3: bool,  # b
    ) -> Tuple[bool, List[Tuple[bytes, bytes, bytes]]]: ...  # (ba(sss))
    def MaskUnitFiles(
        self, arg0: List[bytes], arg1: bool, arg2: bool  # as  # b  # b
    ) -> List[Tuple[bytes, bytes, bytes]]: ...  # a(sss)
    def UnmaskUnitFiles(
        self, arg0: List[bytes], arg1: bool  # as  # b
    ) -> List[Tuple[bytes, bytes, bytes]]: ...  # a(sss)
    def RevertUnitFiles(
        self, arg0: List[bytes]  # as
    ) -> List[Tuple[bytes, bytes, bytes]]: ...  # a(sss)
    def SetDefaultTarget(
        self, arg0: bytes, arg1: bool  # s  # b
    ) -> List[Tuple[bytes, bytes, bytes]]: ...  # a(sss)
    def GetDefaultTarget(self) -> bytes: ...  # s
    def PresetAllUnitFiles(
        self, arg0: bytes, arg1: bool, arg2: bool  # s  # b  # b
    ) -> List[Tuple[bytes, bytes, bytes]]: ...  # a(sss)
    def AddDependencyUnitFiles(
        self,
        arg0: List[bytes],  # as
        arg1: bytes,  # s
        arg2: bytes,  # s
        arg3: bool,  # b
        arg4: bool,  # b
    ) -> List[Tuple[bytes, bytes, bytes]]: ...  # a(sss)
    def GetUnitFileLinks(
        self, arg0: bytes, arg1: bool  # s  # b
    ) -> List[bytes]: ...  # as
    def SetExitCode(self, arg0: int) -> None: ...  # y
    def LookupDynamicUserByName(self, arg0: bytes) -> int: ...  # s  # u
    def LookupDynamicUserByUID(self, arg0: int) -> bytes: ...  # u  # s
    def GetDynamicUsers(self) -> List[Tuple[int, bytes]]: ...  # a(us)

class Manager(SDObject):
    def __init__(self, bus: Optional[DBus] = None, _autoload: bool = False): ...
    def __enter__(self) -> Manager: ...
    Manager: Manager_Manager
