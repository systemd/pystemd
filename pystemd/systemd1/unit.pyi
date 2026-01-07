#
# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Any, AnyStr, List, Optional, Tuple

from pystemd.base import SDInterface, SDObject
from pystemd.dbuslib import DBus

class Unit_Unit(SDInterface):
    ActiveEnterTimestamp: int  # t
    ActiveEnterTimestampMonotonic: int  # t
    ActiveExitTimestamp: int  # t
    ActiveExitTimestampMonotonic: int  # t
    ActiveState: bytes  # s
    After: List[bytes]  # as
    AllowIsolate: bool  # b
    AssertResult: bool  # b
    AssertTimestamp: int  # t
    AssertTimestampMonotonic: int  # t
    Asserts: List[Tuple[bytes, bool, bool, bytes, int]]  # a(sbbsi)
    Before: List[bytes]  # as
    BindsTo: List[bytes]  # as
    BoundBy: List[bytes]  # as
    CanClean: List[bytes]  # as
    CanIsolate: bool  # b
    CanReload: bool  # b
    CanStart: bool  # b
    CanStop: bool  # b
    CollectMode: bytes  # s
    ConditionResult: bool  # b
    ConditionTimestamp: int  # t
    ConditionTimestampMonotonic: int  # t
    Conditions: List[Tuple[bytes, bool, bool, bytes, int]]  # a(sbbsi)
    ConflictedBy: List[bytes]  # as
    Conflicts: List[bytes]  # as
    ConsistsOf: List[bytes]  # as
    DefaultDependencies: bool  # b
    Description: bytes  # s
    Documentation: List[bytes]  # as
    DropInPaths: List[bytes]  # as
    FailureAction: bytes  # s
    FailureActionExitStatus: int  # i
    Following: bytes  # s
    FragmentPath: bytes  # s
    Id: bytes  # s
    IgnoreOnIsolate: bool  # b
    InactiveEnterTimestamp: int  # t
    InactiveEnterTimestampMonotonic: int  # t
    InactiveExitTimestamp: int  # t
    InactiveExitTimestampMonotonic: int  # t
    InvocationID: List[bytes]  # ay
    Job: Tuple[int, bytes]  # (uo)
    JobRunningTimeoutUSec: int  # t
    JobTimeoutAction: bytes  # s
    JobTimeoutRebootArgument: bytes  # s
    JobTimeoutUSec: int  # t
    JoinsNamespaceOf: List[bytes]  # as
    LoadError: Tuple[bytes, bytes]  # (ss)
    LoadState: bytes  # s
    Names: List[bytes]  # as
    NeedDaemonReload: bool  # b
    OnFailure: List[bytes]  # as
    OnFailureJobMode: bytes  # s
    PartOf: List[bytes]  # as
    Perpetual: bool  # b
    PropagatesReloadTo: List[bytes]  # as
    RebootArgument: bytes  # s
    Refs: List[bytes]  # as
    RefuseManualStart: bool  # b
    RefuseManualStop: bool  # b
    ReloadPropagatedFrom: List[bytes]  # as
    RequiredBy: List[bytes]  # as
    Requires: List[bytes]  # as
    RequiresMountsFor: List[bytes]  # as
    Requisite: List[bytes]  # as
    RequisiteOf: List[bytes]  # as
    SourcePath: bytes  # s
    StartLimitAction: bytes  # s
    StartLimitBurst: int  # u
    StartLimitIntervalUSec: int  # t
    StateChangeTimestamp: int  # t
    StateChangeTimestampMonotonic: int  # t
    StopWhenUnneeded: bool  # b
    SubState: bytes  # s
    SuccessAction: bytes  # s
    SuccessActionExitStatus: int  # i
    Transient: bool  # b
    TriggeredBy: List[bytes]  # as
    Triggers: List[bytes]  # as
    UnitFilePreset: bytes  # s
    UnitFileState: bytes  # s
    WantedBy: List[bytes]  # as
    Wants: List[bytes]  # as
    def Start(self, mode: bytes) -> bytes: ...  # s # o
    def Stop(self, mode: bytes) -> bytes: ...  # s # o
    def ResetFailed(self) -> bytes: ...  # s # o
    def Restart(self, mode: bytes) -> bytes: ...  # s # o
    def Reload(self, arg0: bytes) -> bytes: ...  # s  # o
    def TryRestart(self, arg0: bytes) -> bytes: ...  # s  # o
    def ReloadOrRestart(self, arg0: bytes) -> bytes: ...  # s  # o
    def ReloadOrTryRestart(self, arg0: bytes) -> bytes: ...  # s  # o
    def EnqueueJob(
        self,
        arg0: bytes,
        arg1: bytes,  # s  # s
    ) -> Tuple[
        int, bytes, bytes, bytes, bytes, List[Tuple[int, bytes, bytes, bytes, bytes]]
    ]: ...  # (uososa(uosos))
    def Kill(self, arg0: bytes, arg1: int) -> None: ...  # s  # i
    def SetProperties(
        self,
        arg0: bool,
        arg1: List[Tuple[bytes, Any]],  # b  # a(sv)
    ) -> None: ...
    def Ref(self) -> None: ...
    def Unref(self) -> None: ...
    def Clean(self, arg0: List[bytes]) -> None: ...  # as

class Unit_Service(SDInterface):
    AllowedCPUs: List[bytes]  # ay
    AllowedMemoryNodes: List[bytes]  # ay
    AmbientCapabilities: int  # t
    AppArmorProfile: Tuple[bool, bytes]  # (bs)
    BindPaths: List[Tuple[bytes, bytes, bool, int]]  # a(ssbt)
    BindReadOnlyPaths: List[Tuple[bytes, bytes, bool, int]]  # a(ssbt)
    BlockIOAccounting: bool  # b
    BlockIODeviceWeight: List[Tuple[bytes, int]]  # a(st)
    BlockIOReadBandwidth: List[Tuple[bytes, int]]  # a(st)
    BlockIOWeight: int  # t
    BlockIOWriteBandwidth: List[Tuple[bytes, int]]  # a(st)
    BusName: bytes  # s
    CPUAccounting: bool  # b
    CPUAffinity: List[bytes]  # ay
    CPUQuotaPerSecUSec: int  # t
    CPUQuotaPeriodUSec: int  # t
    CPUSchedulingPolicy: int  # i
    CPUSchedulingPriority: int  # i
    CPUSchedulingResetOnFork: bool  # b
    CPUShares: int  # t
    CPUUsageNSec: int  # t
    CPUWeight: int  # t
    CacheDirectory: List[bytes]  # as
    CacheDirectoryMode: int  # u
    CapabilityBoundingSet: int  # t
    CleanResult: bytes  # s
    ConfigurationDirectory: List[bytes]  # as
    ConfigurationDirectoryMode: int  # u
    ControlGroup: bytes  # s
    ControlPID: int  # u
    DefaultMemoryLow: int  # t
    DefaultMemoryMin: int  # t
    Delegate: bool  # b
    DelegateControllers: List[bytes]  # as
    DeviceAllow: List[Tuple[bytes, bytes]]  # a(ss)
    DevicePolicy: bytes  # s
    DisableControllers: List[bytes]  # as
    DynamicUser: bool  # b
    EffectiveCPUs: List[bytes]  # ay
    EffectiveMemoryNodes: List[bytes]  # ay
    Environment: List[bytes]  # as
    EnvironmentFiles: List[Tuple[bytes, bool]]  # a(sb)
    ExecCondition: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecConditionEx: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecMainCode: int  # i
    ExecMainExitTimestamp: int  # t
    ExecMainExitTimestampMonotonic: int  # t
    ExecMainPID: int  # u
    ExecMainStartTimestamp: int  # t
    ExecMainStartTimestampMonotonic: int  # t
    ExecMainStatus: int  # i
    ExecReload: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecReloadEx: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStart: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStartEx: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStartPost: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStartPostEx: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStartPre: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStartPreEx: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStop: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStopEx: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStopPost: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStopPostEx: List[
        Tuple[bytes, List[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    FileDescriptorStoreMax: int  # u
    FinalKillSignal: int  # i
    GID: int  # u
    Group: bytes  # s
    GuessMainPID: bool  # b
    IOAccounting: bool  # b
    IODeviceLatencyTargetUSec: List[Tuple[bytes, int]]  # a(st)
    IODeviceWeight: List[Tuple[bytes, int]]  # a(st)
    IOReadBandwidthMax: List[Tuple[bytes, int]]  # a(st)
    IOReadBytes: int  # t
    IOReadIOPSMax: List[Tuple[bytes, int]]  # a(st)
    IOReadOperations: int  # t
    IOSchedulingClass: int  # i
    IOSchedulingPriority: int  # i
    IOWeight: int  # t
    IOWriteBandwidthMax: List[Tuple[bytes, int]]  # a(st)
    IOWriteBytes: int  # t
    IOWriteIOPSMax: List[Tuple[bytes, int]]  # a(st)
    IOWriteOperations: int  # t
    IPAccounting: bool  # b
    IPAddressAllow: List[Tuple[int, List[bytes], int]]  # a(iayu)
    IPAddressDeny: List[Tuple[int, List[bytes], int]]  # a(iayu)
    IPEgressBytes: int  # t
    IPEgressFilterPath: List[bytes]  # as
    IPEgressPackets: int  # t
    IPIngressBytes: int  # t
    IPIngressFilterPath: List[bytes]  # as
    IPIngressPackets: int  # t
    IgnoreSIGPIPE: bool  # b
    InaccessiblePaths: List[bytes]  # as
    KeyringMode: bytes  # s
    KillMode: bytes  # s
    KillSignal: int  # i
    LimitAS: int  # t
    LimitASSoft: int  # t
    LimitCORE: int  # t
    LimitCORESoft: int  # t
    LimitCPU: int  # t
    LimitCPUSoft: int  # t
    LimitDATA: int  # t
    LimitDATASoft: int  # t
    LimitFSIZE: int  # t
    LimitFSIZESoft: int  # t
    LimitLOCKS: int  # t
    LimitLOCKSSoft: int  # t
    LimitMEMLOCK: int  # t
    LimitMEMLOCKSoft: int  # t
    LimitMSGQUEUE: int  # t
    LimitMSGQUEUESoft: int  # t
    LimitNICE: int  # t
    LimitNICESoft: int  # t
    LimitNOFILE: int  # t
    LimitNOFILESoft: int  # t
    LimitNPROC: int  # t
    LimitNPROCSoft: int  # t
    LimitRSS: int  # t
    LimitRSSSoft: int  # t
    LimitRTPRIO: int  # t
    LimitRTPRIOSoft: int  # t
    LimitRTTIME: int  # t
    LimitRTTIMESoft: int  # t
    LimitSIGPENDING: int  # t
    LimitSIGPENDINGSoft: int  # t
    LimitSTACK: int  # t
    LimitSTACKSoft: int  # t
    LockPersonality: bool  # b
    LogExtraFields: List[List[bytes]]  # aay
    LogLevelMax: int  # i
    LogRateLimitBurst: int  # u
    LogRateLimitIntervalUSec: int  # t
    LogsDirectory: List[bytes]  # as
    LogsDirectoryMode: int  # u
    MainPID: int  # u
    MemoryAccounting: bool  # b
    MemoryCurrent: int  # t
    MemoryDenyWriteExecute: bool  # b
    MemoryHigh: int  # t
    MemoryLimit: int  # t
    MemoryLow: int  # t
    MemoryMax: int  # t
    MemoryMin: int  # t
    MemorySwapMax: int  # t
    MountAPIVFS: bool  # b
    MountFlags: int  # t
    NFileDescriptorStore: int  # u
    NRestarts: int  # u
    NUMAMask: List[bytes]  # ay
    NUMAPolicy: int  # i
    NetworkNamespacePath: bytes  # s
    Nice: int  # i
    NoNewPrivileges: bool  # b
    NonBlocking: bool  # b
    NotifyAccess: bytes  # s
    OOMPolicy: bytes  # s
    OOMScoreAdjust: int  # i
    PAMName: bytes  # s
    PIDFile: bytes  # s
    PassEnvironment: List[bytes]  # as
    Personality: bytes  # s
    PrivateDevices: bool  # b
    PrivateMounts: bool  # b
    PrivateNetwork: bool  # b
    PrivateTmp: bool  # b
    PrivateUsers: bool  # b
    ProtectControlGroups: bool  # b
    ProtectHome: bytes  # s
    ProtectHostname: bool  # b
    ProtectKernelLogs: bool  # b
    ProtectKernelModules: bool  # b
    ProtectKernelTunables: bool  # b
    ProtectSystem: bytes  # s
    ReadOnlyPaths: List[bytes]  # as
    ReadWritePaths: List[bytes]  # as
    ReloadResult: bytes  # s
    RemainAfterExit: bool  # b
    RemoveIPC: bool  # b
    Restart: bytes  # s
    RestartForceExitStatus: Tuple[List[int], List[int]]  # (aiai)
    RestartKillSignal: int  # i
    RestartPreventExitStatus: Tuple[List[int], List[int]]  # (aiai)
    RestartUSec: int  # t
    RestrictAddressFamilies: Tuple[bool, List[bytes]]  # (bas)
    RestrictNamespaces: int  # t
    RestrictRealtime: bool  # b
    RestrictSUIDSGID: bool  # b
    Result: bytes  # s
    RootDirectory: bytes  # s
    RootDirectoryStartOnly: bool  # b
    RootImage: bytes  # s
    RuntimeDirectory: List[bytes]  # as
    RuntimeDirectoryMode: int  # u
    RuntimeDirectoryPreserve: bytes  # s
    RuntimeMaxUSec: int  # t
    SELinuxContext: Tuple[bool, bytes]  # (bs)
    SameProcessGroup: bool  # b
    SecureBits: int  # i
    SendSIGHUP: bool  # b
    SendSIGKILL: bool  # b
    Slice: bytes  # s
    SmackProcessLabel: Tuple[bool, bytes]  # (bs)
    StandardError: bytes  # s
    StandardErrorFileDescriptorName: bytes  # s
    StandardInput: bytes  # s
    StandardInputData: List[bytes]  # ay
    StandardInputFileDescriptorName: bytes  # s
    StandardOutput: bytes  # s
    StandardOutputFileDescriptorName: bytes  # s
    StartupBlockIOWeight: int  # t
    StartupCPUShares: int  # t
    StartupCPUWeight: int  # t
    StartupIOWeight: int  # t
    StateDirectory: List[bytes]  # as
    StateDirectoryMode: int  # u
    StatusErrno: int  # i
    StatusText: bytes  # s
    SuccessExitStatus: Tuple[List[int], List[int]]  # (aiai)
    SupplementaryGroups: List[bytes]  # as
    SyslogFacility: int  # i
    SyslogIdentifier: bytes  # s
    SyslogLevel: int  # i
    SyslogLevelPrefix: bool  # b
    SyslogPriority: int  # i
    SystemCallArchitectures: List[bytes]  # as
    SystemCallErrorNumber: int  # i
    SystemCallFilter: Tuple[bool, List[bytes]]  # (bas)
    TTYPath: bytes  # s
    TTYReset: bool  # b
    TTYVHangup: bool  # b
    TTYVTDisallocate: bool  # b
    TasksAccounting: bool  # b
    TasksCurrent: int  # t
    TasksMax: int  # t
    TemporaryFileSystem: List[Tuple[bytes, bytes]]  # a(ss)
    TimeoutAbortUSec: int  # t
    TimeoutCleanUSec: int  # t
    TimeoutStartUSec: int  # t
    TimeoutStopUSec: int  # t
    TimerSlackNSec: int  # t
    Type: bytes  # s
    UID: int  # u
    UMask: int  # u
    USBFunctionDescriptors: bytes  # s
    USBFunctionStrings: bytes  # s
    UnsetEnvironment: List[bytes]  # as
    User: bytes  # s
    UtmpIdentifier: bytes  # s
    UtmpMode: bytes  # s
    WatchdogSignal: int  # i
    WatchdogTimestamp: int  # t
    WatchdogTimestampMonotonic: int  # t
    WatchdogUSec: int  # t
    WorkingDirectory: bytes  # s
    def GetProcesses(self) -> List[Tuple[bytes, int, bytes]]: ...  # a(sus)
    def AttachProcesses(self, arg0: bytes, arg1: List[int]) -> None: ...  # s  # au

class Unit(SDObject):
    def __init__(
        self, external_id: AnyStr, bus: Optional[DBus] = None, _autoload: bool = False
    ): ...
    def __enter__(self) -> Unit: ...
    Unit: Unit_Unit
    Service: Unit_Service
