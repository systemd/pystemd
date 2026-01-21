#
# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from __future__ import annotations

from typing import Any, AnyStr

from pystemd.base import SDInterface, SDObject
from pystemd.dbuslib import DBus

class Unit_Unit(SDInterface):
    AccessSELinuxContext: bytes  # s
    ActivationDetails: list[tuple[bytes, bytes]]  # a(ss)
    ActiveEnterTimestamp: int  # t
    ActiveEnterTimestampMonotonic: int  # t
    ActiveExitTimestamp: int  # t
    ActiveExitTimestampMonotonic: int  # t
    ActiveState: bytes  # s
    After: list[bytes]  # as
    AllowIsolate: bool  # b
    AssertResult: bool  # b
    AssertTimestamp: int  # t
    AssertTimestampMonotonic: int  # t
    Asserts: list[tuple[bytes, bool, bool, bytes, int]]  # a(sbbsi)
    Before: list[bytes]  # as
    BindsTo: list[bytes]  # as
    BoundBy: list[bytes]  # as
    CanClean: list[bytes]  # as
    CanFreeze: bool  # b
    CanIsolate: bool  # b
    CanLiveMount: bool  # b
    CanReload: bool  # b
    CanStart: bool  # b
    CanStop: bool  # b
    CollectMode: bytes  # s
    ConditionResult: bool  # b
    ConditionTimestamp: int  # t
    ConditionTimestampMonotonic: int  # t
    Conditions: list[tuple[bytes, bool, bool, bytes, int]]  # a(sbbsi)
    ConflictedBy: list[bytes]  # as
    Conflicts: list[bytes]  # as
    ConsistsOf: list[bytes]  # as
    DebugInvocation: bool  # b
    DefaultDependencies: bool  # b
    Description: bytes  # s
    Documentation: list[bytes]  # as
    DropInPaths: list[bytes]  # as
    FailureAction: bytes  # s
    FailureActionExitStatus: int  # i
    Following: bytes  # s
    FragmentPath: bytes  # s
    FreezerState: bytes  # s
    Id: bytes  # s
    IgnoreOnIsolate: bool  # b
    InactiveEnterTimestamp: int  # t
    InactiveEnterTimestampMonotonic: int  # t
    InactiveExitTimestamp: int  # t
    InactiveExitTimestampMonotonic: int  # t
    InvocationID: list[bytes]  # ay
    Job: tuple[int, bytes]  # (uo)
    JobRunningTimeoutUSec: int  # t
    JobTimeoutAction: bytes  # s
    JobTimeoutRebootArgument: bytes  # s
    JobTimeoutUSec: int  # t
    JoinsNamespaceOf: list[bytes]  # as
    LoadError: tuple[bytes, bytes]  # (ss)
    LoadState: bytes  # s
    Markers: list[bytes]  # as
    Names: list[bytes]  # as
    NeedDaemonReload: bool  # b
    OnFailure: list[bytes]  # as
    OnFailureJobMode: bytes  # s
    OnFailureOf: list[bytes]  # as
    OnSuccess: list[bytes]  # as
    OnSuccessJobMode: bytes  # s
    OnSuccessOf: list[bytes]  # as
    PartOf: list[bytes]  # as
    Perpetual: bool  # b
    PropagatesReloadTo: list[bytes]  # as
    PropagatesStopTo: list[bytes]  # as
    RebootArgument: bytes  # s
    Refs: list[bytes]  # as
    RefuseManualStart: bool  # b
    RefuseManualStop: bool  # b
    ReloadPropagatedFrom: list[bytes]  # as
    RequiredBy: list[bytes]  # as
    Requires: list[bytes]  # as
    RequiresMountsFor: list[bytes]  # as
    Requisite: list[bytes]  # as
    RequisiteOf: list[bytes]  # as
    SliceOf: list[bytes]  # as
    SourcePath: bytes  # s
    StartLimitAction: bytes  # s
    StartLimitBurst: int  # u
    StartLimitIntervalUSec: int  # t
    StateChangeTimestamp: int  # t
    StateChangeTimestampMonotonic: int  # t
    StopPropagatedFrom: list[bytes]  # as
    StopWhenUnneeded: bool  # b
    SubState: bytes  # s
    SuccessAction: bytes  # s
    SuccessActionExitStatus: int  # i
    SurviveFinalKillSignal: bool  # b
    Transient: bool  # b
    TriggeredBy: list[bytes]  # as
    Triggers: list[bytes]  # as
    UnitFilePreset: bytes  # s
    UnitFileState: bytes  # s
    UpheldBy: list[bytes]  # as
    Upholds: list[bytes]  # as
    WantedBy: list[bytes]  # as
    Wants: list[bytes]  # as
    WantsMountsFor: list[bytes]  # as
    def Clean(self, arg0: list[bytes]) -> None: ...  # as
    def EnqueueJob(
        self,
        arg0: bytes,
        arg1: bytes,  # s  # s
    ) -> tuple[
        int, bytes, bytes, bytes, bytes, list[tuple[int, bytes, bytes, bytes, bytes]]
    ]: ...  # (uososa(uosos))
    def Freeze(self) -> None: ...
    def Kill(self, arg0: bytes, arg1: int) -> None: ...  # s  # i
    def KillSubgroup(self, arg0: bytes, arg1: int) -> None: ...  # s  # i
    def QueueSignal(self, arg0: bytes, arg1: int, arg2: int) -> None: ...  # s  # i  # i
    def Ref(self) -> None: ...
    def Reload(self, arg0: bytes) -> bytes: ...  # s  # o
    def ReloadOrRestart(self, arg0: bytes) -> bytes: ...  # s  # o
    def ReloadOrTryRestart(self, arg0: bytes) -> bytes: ...  # s  # o
    def ResetFailed(self) -> None: ...
    def Restart(self, mode: bytes) -> bytes: ...  # s # o
    def SetProperties(
        self,
        arg0: bool,
        arg1: list[tuple[bytes, Any]],  # b  # a(sv)
    ) -> None: ...
    def Start(self, mode: bytes) -> bytes: ...  # s # o
    def Stop(self, mode: bytes) -> bytes: ...  # s # o
    def Thaw(self) -> None: ...
    def TryRestart(self, arg0: bytes) -> bytes: ...  # s  # o
    def Unref(self) -> None: ...

class Unit_Service(SDInterface):
    AllowedCPUs: list[bytes]  # ay
    AllowedMemoryNodes: list[bytes]  # ay
    AmbientCapabilities: int  # t
    AppArmorProfile: tuple[bool, bytes]  # (bs)
    BPFDelegateAttachments: bytes  # s
    BPFDelegateCommands: bytes  # s
    BPFDelegateMaps: bytes  # s
    BPFDelegatePrograms: bytes  # s
    BPFProgram: list[tuple[bytes, bytes]]  # a(ss)
    BindLogSockets: bool  # b
    BindPaths: list[tuple[bytes, bytes, bool, int]]  # a(ssbt)
    BindReadOnlyPaths: list[tuple[bytes, bytes, bool, int]]  # a(ssbt)
    BlockIOAccounting: bool  # b
    BlockIODeviceWeight: list[tuple[bytes, int]]  # a(st)
    BlockIOReadBandwidth: list[tuple[bytes, int]]  # a(st)
    BlockIOWeight: int  # t
    BlockIOWriteBandwidth: list[tuple[bytes, int]]  # a(st)
    BusName: bytes  # s
    CPUAccounting: bool  # b
    CPUAffinity: list[bytes]  # ay
    CPUAffinityFromNUMA: bool  # b
    CPUQuotaPerSecUSec: int  # t
    CPUQuotaPeriodUSec: int  # t
    CPUSchedulingPolicy: int  # i
    CPUSchedulingPriority: int  # i
    CPUSchedulingResetOnFork: bool  # b
    CPUShares: int  # t
    CPUUsageNSec: int  # t
    CPUWeight: int  # t
    CacheDirectory: list[bytes]  # as
    CacheDirectoryAccounting: bool  # b
    CacheDirectoryMode: int  # u
    CacheDirectoryQuota: tuple[int, int, bytes]  # (tus)
    CacheDirectoryQuotaUsage: tuple[int, int]  # (tt)
    CacheDirectorySymlink: list[tuple[bytes, bytes, int]]  # a(sst)
    CapabilityBoundingSet: int  # t
    CleanResult: bytes  # s
    ConfigurationDirectory: list[bytes]  # as
    ConfigurationDirectoryMode: int  # u
    ControlGroup: bytes  # s
    ControlGroupId: int  # t
    ControlPID: int  # u
    CoredumpFilter: int  # t
    CoredumpReceive: bool  # b
    DefaultMemoryLow: int  # t
    DefaultMemoryMin: int  # t
    DefaultStartupMemoryLow: int  # t
    Delegate: bool  # b
    DelegateControllers: list[bytes]  # as
    DelegateNamespaces: int  # t
    DelegateSubgroup: bytes  # s
    DeviceAllow: list[tuple[bytes, bytes]]  # a(ss)
    DevicePolicy: bytes  # s
    DisableControllers: list[bytes]  # as
    DynamicUser: bool  # b
    EffectiveCPUs: list[bytes]  # ay
    EffectiveMemoryHigh: int  # t
    EffectiveMemoryMax: int  # t
    EffectiveMemoryNodes: list[bytes]  # ay
    EffectiveTasksMax: int  # t
    Environment: list[bytes]  # as
    EnvironmentFiles: list[tuple[bytes, bool]]  # a(sb)
    ExecCondition: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecConditionEx: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecMainCode: int  # i
    ExecMainExitTimestamp: int  # t
    ExecMainExitTimestampMonotonic: int  # t
    ExecMainHandoffTimestamp: int  # t
    ExecMainHandoffTimestampMonotonic: int  # t
    ExecMainPID: int  # u
    ExecMainStartTimestamp: int  # t
    ExecMainStartTimestampMonotonic: int  # t
    ExecMainStatus: int  # i
    ExecPaths: list[bytes]  # as
    ExecReload: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecReloadEx: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecSearchPath: list[bytes]  # as
    ExecStart: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStartEx: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStartPost: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStartPostEx: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStartPre: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStartPreEx: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStop: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStopEx: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStopPost: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExecStopPostEx: list[
        tuple[bytes, list[bytes], bool, int, int, int, int, int, int, int]
    ]  # a(sasbttttuii)
    ExitType: bytes  # s
    ExtensionDirectories: list[bytes]  # as
    ExtensionImagePolicy: bytes  # s
    ExtensionImages: list[tuple[bytes, bool, list[tuple[bytes, bytes]]]]  # a(sba(ss))
    ExtraFileDescriptorNames: list[bytes]  # as
    FileDescriptorStoreMax: int  # u
    FileDescriptorStorePreserve: bytes  # s
    FinalKillSignal: int  # i
    GID: int  # u
    Group: bytes  # s
    GuessMainPID: bool  # b
    IOAccounting: bool  # b
    IODeviceLatencyTargetUSec: list[tuple[bytes, int]]  # a(st)
    IODeviceWeight: list[tuple[bytes, int]]  # a(st)
    IOReadBandwidthMax: list[tuple[bytes, int]]  # a(st)
    IOReadBytes: int  # t
    IOReadIOPSMax: list[tuple[bytes, int]]  # a(st)
    IOReadOperations: int  # t
    IOSchedulingClass: int  # i
    IOSchedulingPriority: int  # i
    IOWeight: int  # t
    IOWriteBandwidthMax: list[tuple[bytes, int]]  # a(st)
    IOWriteBytes: int  # t
    IOWriteIOPSMax: list[tuple[bytes, int]]  # a(st)
    IOWriteOperations: int  # t
    IPAccounting: bool  # b
    IPAddressAllow: list[tuple[int, list[bytes], int]]  # a(iayu)
    IPAddressDeny: list[tuple[int, list[bytes], int]]  # a(iayu)
    IPCNamespacePath: bytes  # s
    IPEgressBytes: int  # t
    IPEgressFilterPath: list[bytes]  # as
    IPEgressPackets: int  # t
    IPIngressBytes: int  # t
    IPIngressFilterPath: list[bytes]  # as
    IPIngressPackets: int  # t
    IgnoreSIGPIPE: bool  # b
    ImportCredential: list[bytes]  # as
    ImportCredentialEx: list[tuple[bytes, bytes]]  # a(ss)
    InaccessiblePaths: list[bytes]  # as
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
    LiveMountResult: bytes  # s
    LoadCredential: list[tuple[bytes, bytes]]  # a(ss)
    LoadCredentialEncrypted: list[tuple[bytes, bytes]]  # a(ss)
    LockPersonality: bool  # b
    LogExtraFields: list[list[bytes]]  # aay
    LogFilterPatterns: list[tuple[bool, bytes]]  # a(bs)
    LogLevelMax: int  # i
    LogNamespace: bytes  # s
    LogRateLimitBurst: int  # u
    LogRateLimitIntervalUSec: int  # t
    LogsDirectory: list[bytes]  # as
    LogsDirectoryAccounting: bool  # b
    LogsDirectoryMode: int  # u
    LogsDirectoryQuota: tuple[int, int, bytes]  # (tus)
    LogsDirectoryQuotaUsage: tuple[int, int]  # (tt)
    LogsDirectorySymlink: list[tuple[bytes, bytes, int]]  # a(sst)
    MainPID: int  # u
    ManagedOOMMemoryPressure: bytes  # s
    ManagedOOMMemoryPressureDurationUSec: int  # t
    ManagedOOMMemoryPressureLimit: int  # u
    ManagedOOMPreference: bytes  # s
    ManagedOOMSwap: bytes  # s
    MemoryAccounting: bool  # b
    MemoryAvailable: int  # t
    MemoryCurrent: int  # t
    MemoryDenyWriteExecute: bool  # b
    MemoryHigh: int  # t
    MemoryKSM: bool  # b
    MemoryLow: int  # t
    MemoryLimit: int  # t
    MemoryMax: int  # t
    MemoryMin: int  # t
    MemoryPeak: int  # t
    MemoryPressureThresholdUSec: int  # t
    MemoryPressureWatch: bytes  # s
    MemorySwapCurrent: int  # t
    MemorySwapMax: int  # t
    MemorySwapPeak: int  # t
    MemoryZSwapCurrent: int  # t
    MemoryZSwapMax: int  # t
    MemoryZSwapWriteback: bool  # b
    MountAPIVFS: bool  # b
    MountFlags: int  # t
    MountImagePolicy: bytes  # s
    MountImages: list[
        tuple[bytes, bytes, bool, list[tuple[bytes, bytes]]]
    ]  # a(ssba(ss))
    NFTSet: list[tuple[int, int, bytes, bytes]]  # a(iiss)
    NFileDescriptorStore: int  # u
    NRestarts: int  # u
    NUMAMask: list[bytes]  # ay
    NUMAPolicy: int  # i
    NetworkNamespacePath: bytes  # s
    Nice: int  # i
    NoExecPaths: list[bytes]  # as
    NoNewPrivileges: bool  # b
    NonBlocking: bool  # b
    NotifyAccess: bytes  # s
    OOMPolicy: bytes  # s
    OOMScoreAdjust: int  # i
    OpenFile: list[tuple[bytes, bytes, int]]  # a(sst)
    PAMName: bytes  # s
    PIDFile: bytes  # s
    PassEnvironment: list[bytes]  # as
    Personality: bytes  # s
    PrivateBPF: bytes  # s
    PrivateDevices: bool  # b
    PrivateIPC: bool  # b
    PrivateMounts: bool  # b
    PrivateNetwork: bool  # b
    PrivatePIDs: bytes  # s
    PrivateTmp: bool  # b
    PrivateTmpEx: bytes  # s
    PrivateUsers: bool  # b
    PrivateUsersEx: bytes  # s
    ProcSubset: bytes  # s
    ProtectClock: bool  # b
    ProtectControlGroups: bool  # b
    ProtectControlGroupsEx: bytes  # s
    ProtectHome: bytes  # s
    ProtectHostname: bool  # b
    ProtectHostnameEx: tuple[bytes, bytes]  # (ss)
    ProtectKernelLogs: bool  # b
    ProtectKernelModules: bool  # b
    ProtectKernelTunables: bool  # b
    ProtectProc: bytes  # s
    ProtectSystem: bytes  # s
    ReadOnlyPaths: list[bytes]  # as
    ReadWritePaths: list[bytes]  # as
    ReloadResult: bytes  # s
    ReloadSignal: int  # i
    RemainAfterExit: bool  # b
    RemoveIPC: bool  # b
    Restart: bytes  # s
    RestartForceExitStatus: tuple[list[int], list[int]]  # (aiai)
    RestartKillSignal: int  # i
    RestartMaxDelayUSec: int  # t
    RestartMode: bytes  # s
    RestartPreventExitStatus: tuple[list[int], list[int]]  # (aiai)
    RestartSteps: int  # u
    RestartUSec: int  # t
    RestartUSecNext: int  # t
    RestrictAddressFamilies: tuple[bool, list[bytes]]  # (bas)
    RestrictFileSystems: tuple[bool, list[bytes]]  # (bas)
    RestrictNamespaces: int  # t
    RestrictNetworkInterfaces: tuple[bool, list[bytes]]  # (bas)
    RestrictRealtime: bool  # b
    RestrictSUIDSGID: bool  # b
    Result: bytes  # s
    RootDirectory: bytes  # s
    RootDirectoryStartOnly: bool  # b
    RootEphemeral: bool  # b
    RootHash: list[bytes]  # ay
    RootHashPath: bytes  # s
    RootHashSignature: list[bytes]  # ay
    RootHashSignaturePath: bytes  # s
    RootImage: bytes  # s
    RootImageOptions: list[tuple[bytes, bytes]]  # a(ss)
    RootImagePolicy: bytes  # s
    RootVerity: bytes  # s
    RuntimeDirectory: list[bytes]  # as
    RuntimeDirectoryMode: int  # u
    RuntimeDirectoryPreserve: bytes  # s
    RuntimeDirectorySymlink: list[tuple[bytes, bytes, int]]  # a(sst)
    RuntimeMaxUSec: int  # t
    RuntimeRandomizedExtraUSec: int  # t
    SELinuxContext: tuple[bool, bytes]  # (bs)
    SameProcessGroup: bool  # b
    SecureBits: int  # i
    SendSIGHUP: bool  # b
    SendSIGKILL: bool  # b
    SetCredential: list[tuple[bytes, list[bytes]]]  # a(say)
    SetCredentialEncrypted: list[tuple[bytes, list[bytes]]]  # a(say)
    SetLoginEnvironment: bool  # b
    Slice: bytes  # s
    SmackProcessLabel: tuple[bool, bytes]  # (bs)
    SocketBindAllow: list[tuple[int, int, int, int]]  # a(iiqq)
    SocketBindDeny: list[tuple[int, int, int, int]]  # a(iiqq)
    StandardError: bytes  # s
    StandardErrorFileDescriptorName: bytes  # s
    StandardInput: bytes  # s
    StandardInputData: list[bytes]  # ay
    StandardInputFileDescriptorName: bytes  # s
    StandardOutput: bytes  # s
    StandardOutputFileDescriptorName: bytes  # s
    StartupAllowedCPUs: list[bytes]  # ay
    StartupAllowedMemoryNodes: list[bytes]  # ay
    StartupBlockIOWeight: int  # t
    StartupCPUShares: int  # t
    StartupCPUWeight: int  # t
    StartupIOWeight: int  # t
    StartupMemoryHigh: int  # t
    StartupMemoryLow: int  # t
    StartupMemoryMax: int  # t
    StartupMemorySwapMax: int  # t
    StartupMemoryZSwapMax: int  # t
    StateDirectory: list[bytes]  # as
    StateDirectoryAccounting: bool  # b
    StateDirectoryMode: int  # u
    StateDirectoryQuota: tuple[int, int, bytes]  # (tus)
    StateDirectoryQuotaUsage: tuple[int, int]  # (tt)
    StateDirectorySymlink: list[tuple[bytes, bytes, int]]  # a(sst)
    StatusBusError: bytes  # s
    StatusErrno: int  # i
    StatusText: bytes  # s
    StatusVarlinkError: bytes  # s
    SuccessExitStatus: tuple[list[int], list[int]]  # (aiai)
    SupplementaryGroups: list[bytes]  # as
    SyslogFacility: int  # i
    SyslogIdentifier: bytes  # s
    SyslogLevel: int  # i
    SyslogLevelPrefix: bool  # b
    SyslogPriority: int  # i
    SystemCallArchitectures: list[bytes]  # as
    SystemCallErrorNumber: int  # i
    SystemCallFilter: tuple[bool, list[bytes]]  # (bas)
    SystemCallLog: tuple[bool, list[bytes]]  # (bas)
    TTYColumns: int  # q
    TTYPath: bytes  # s
    TTYReset: bool  # b
    TTYRows: int  # q
    TTYVHangup: bool  # b
    TTYVTDisallocate: bool  # b
    TasksAccounting: bool  # b
    TasksCurrent: int  # t
    TasksMax: int  # t
    TemporaryFileSystem: list[tuple[bytes, bytes]]  # a(ss)
    TimeoutAbortUSec: int  # t
    TimeoutCleanUSec: int  # t
    TimeoutStartFailureMode: bytes  # s
    TimeoutStartUSec: int  # t
    TimeoutStopFailureMode: bytes  # s
    TimeoutStopUSec: int  # t
    TimerSlackNSec: int  # t
    Type: bytes  # s
    UID: int  # u
    UMask: int  # u
    USBFunctionDescriptors: bytes  # s
    USBFunctionStrings: bytes  # s
    UnsetEnvironment: list[bytes]  # as
    User: bytes  # s
    UtmpIdentifier: bytes  # s
    UtmpMode: bytes  # s
    WatchdogSignal: int  # i
    WatchdogTimestamp: int  # t
    WatchdogTimestampMonotonic: int  # t
    WatchdogUSec: int  # t
    WorkingDirectory: bytes  # s
    def AttachProcesses(self, arg0: bytes, arg1: list[int]) -> None: ...  # s  # au
    def BindMount(
        self, arg0: bytes, arg1: bytes, arg2: bool, arg3: bool
    ) -> None: ...  # s  # s  # b  # b
    def DumpFileDescriptorStore(
        self,
    ) -> list[
        tuple[bytes, int, int, int, int, int, int, bytes, int]
    ]: ...  # a(suuutuusu)
    def GetProcesses(self) -> list[tuple[bytes, int, bytes]]: ...  # a(sus)
    def MountImage(
        self,
        arg0: bytes,
        arg1: bytes,
        arg2: bool,
        arg3: bool,
        arg4: list[tuple[bytes, bytes]],
    ) -> None: ...  # s  # s  # b  # b  # a(ss)
    def RemoveSubgroup(self, arg0: bytes, arg1: int) -> None: ...  # s  # t

class Unit(SDObject):
    def __init__(
        self, external_id: AnyStr, bus: DBus | None = None, _autoload: bool = False
    ): ...
    def __enter__(self) -> Unit: ...
    Unit: Unit_Unit
    Service: Unit_Service
