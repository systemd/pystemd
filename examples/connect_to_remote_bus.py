import os

from pystemd.dbuslib import DBusRemote
from pystemd.systemd1 import Unit


def full_example():
    # DBusRemote will use ssh to connect to another bus, so whatever a valid ssh conection
    # string is, we can use it, you could also use DBusAddress, but thats harder
    with DBusRemote(b"localhost") as bus, Unit(b"postfix.service", bus=bus) as sd_unit:
        print("ConditionTimestamp", sd_unit.Unit.ConditionTimestamp)
        print("StopWhenUnneeded", sd_unit.Unit.StopWhenUnneeded)
        print("StartLimitAction", sd_unit.Unit.StartLimitAction)
        print("StartLimitBurst", sd_unit.Unit.StartLimitBurst)
        print("StartupBlockIOWeight", sd_unit.Service.StartupBlockIOWeight)
        print("SyslogPriority", sd_unit.Service.SyslogPriority)
        print("SyslogFacility", sd_unit.Service.SyslogFacility)
        print("SyslogLevelPrefix", sd_unit.Service.SyslogLevelPrefix)
        print("After", sd_unit.Unit.After)
        print("Conditions", sd_unit.Unit.Conditions)
        print("Job", sd_unit.Unit.Job)
        print("InvocationID", sd_unit.Unit.InvocationID)
        print("ExecStart", sd_unit.Service.ExecStart)

        # next one require sudo powers!
        if os.geteuid() == 0:
            print(".GetProcesses", sd_unit.Service.GetProcesses())
            print(".Start(b'replace')", sd_unit.Unit.Start(b"replace"))
        else:
            print("no root user, no complex method for you!")


if __name__ == "__main__":
    full_example()
