#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

"""

This library allows you to talk to systemd over dbus from python, without
actually thinking that you are talking to systemd over dbus. This is focus so
you can programatically, start/stop/restart/kill and verify services status from
systemd point of view, and avoiding `subprocess.Popen(['systemctl', ...`

Usage in interactive mode:

    In [1]: from pystemd.systemd1 import Unit as SDUnit
    In [2]: unit = SDUnit(b'postfix.service')
    In [3]: unit.load()

    # on real code you do In [2,3] in a single line with
    #     with SDUnit(b'postfix.service') as unit:
    #         ... do your code

    In [4]: unit.Unit.ActiveState
    Out[4]: b'active'

    In [5]: unit.Unit.StopWhenUnneeded
    Out[5]: False

    In [6]: unit.Unit.Stop(b'replace') # require privilege account
    Out[6]: b'/org/freedesktop/systemd1/job/6601531'

    In [7]: unit.Unit.ActiveState
    Out[7]: b'inactive'

    In [8]: unit.Unit.Start(b'replace') # require privilege account
    Out[8]: b'/org/freedesktop/systemd1/job/6601532'

    In [9]: unit.Unit.ActiveState
    Out[9]: b'active'

    In [10]: unit.Service.GetProcesses()
    Out[10]:
    [(b'/system.slice/postfix.service',
        1754222,
        b'/usr/libexec/postfix/master -w'),
     (b'/system.slice/postfix.service', 1754224, b'pickup -l -t fifo -u'),
     (b'/system.slice/postfix.service', 1754225, b'qmgr -l -t fifo -u')]

    # Tons of Extra information, examples

    In [11]: unit.Unit.Description
    Out[11]: b'Postfix Mail Transport Agent'

    In [12]: unit.Service.MainPID
    Out[12]: 1754222

    In [13]: unit.Service.PIDFile
    Out[13]: b'/var/spool/postfix/pid/master.pid'


Note a few things:
  1.- This is python3 example.
  2.- We dont really use strings, but bytes.
  3.- Type information is not lost, Out[5] is a boolean, and Out[10] is an
       array of tuples, and each tuple is a (bytes, int, bytes)
  4.- There are a few interfaces to interact, for instance here you saw
      `unit.Unit` and `unit.Service`, There are more interfaces, you can look
      unit.interfaces for a list of them.

      4.1.- Each interface has methods and properties, They can be inspected
        in the commandline, or by inspecting
        `unit.interfaces[<interface>].methods` or
        `unit.interfaces[<interface>].properties`
      4.2.- Properties are read-only.

Extra read (mostly if you want to develop or extend this):

    http://0pointer.net/blog/the-new-sd-bus-api-of-systemd.html : example and
     c code, introduction to busctl.
    https://www.freedesktop.org/wiki/Software/systemd/dbus/ : intro to the
     manager interface.

    some common commandline tools that are useful to know how things are done:

      https://github.com/systemd/systemd/blob/master/src/systemctl/systemctl.c
      https://github.com/systemd/systemd/blob/master/src/busctl/busctl.c
      https://github.com/systemd/systemd/blob/master/src/systemd/sd-bus.h
      https://github.com/systemd/systemd/blob/master/src/libsystemd/sd-bus/sd-bus.c

    similar library but with a diferent aproach (they hardcode all the method
    they want). https://github.com/wiliamsouza/python-systemd . with that said.
    this is build in a way that we can extend the Base Classes to have hardcoded
    methods (example we can have SDUnit.Start that calls SDUnit.Unit.Start)

    some man pages:
        https://www.freedesktop.org/software/systemd/man/index.html#S
"""

from pystemd import DBus, __version__, machine1, systemd1


# handy shortcuts for systemd resources
SDUnit = systemd1.Unit
SDManager = systemd1.Manager
SDMachine = machine1.Machine

__all__ = ["systemd1", "machine1", "__version__", "DBus"]
