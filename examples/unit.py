#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

"""
This is a set of example of stuff you could do with a SDUnit object
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from pystemd.unit import SDUnit


def full_example():
    with SDUnit(b"postfix.service") as sd_unit:
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

        print(sd_unit.Service._methods_xml["GetProcesses"].toxml())
