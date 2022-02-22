Changelog
---------

We annotate all changes here, keep in mind that the high version may not be
the one you find pypi, but its the one in development.

0.11.0
=====
* native support for stop_cmd, (pre|post)_start_cmd and post_stop_cmd in pystemd.run.
* adding lxml as a dependency.
* drop support for python 3.4 and 3.5 (yey welcome f-strings)

0.10.0
=====
* support for interactive auth.

0.9.0
=====
* add initial support for Python 3.9
* include .pxd and .pxi files in the source distribution

0.8.0
=====
* add initial support for python 3.7 and 3.8
* added options StandardOutputFile, StandardOutputFileToAppend, StandardErrorFile and
  StandardErrorFileToAppend to known unit signatures.
* Added type stubs for `pystemd.daemon`, `pystemd.dbuslib`, `pystemd.systemd1.Unit`
  and `pystemd.systemd1.Manager` because we still "support python 3.4.
* fix issue when char is unsigned, and <char *> -1 returns 255.
* added `slice_` option to pystemd.run to specify the cgroup where the unit is created.

0.7.0
=====
* Modify README to show the right systemd min version.
* Added `pystemd.journal` with methods `log` and `sendv`.
* Added `booted` support in `pystemd.daemon` to know if a system was booted with
  systemd.
* allow None (translated to NULL) options in DBUS.match_signal.
* Added `address` option to `pystemd.run` to support custom dbus addresses.
* Added `socket` options to unit_signatures, now we can create transient sockets.

0.6.0
=====
* Improve in-repo docs.
* changed license from BSD to LGPL-2.1+.
* Raise `DBusInterruptedError` instead of `DBusBaseError` when a system call is
  interrupted.
* expose sd_bus_match_signal as Dbus.match_signal for easy monitoring of the bus.
* Drop python 2 support and six requirement.
* Auto convert Path object to bytes so that can be passed to dbus.
* Add service_type to pystemd.run for easy Type selection.
* Many new DBus properties.
* access interface methods and properties directly.
* systemd1.Manager.StartTransientUnit now support extra units, allowing users
  to also create timer/path transient units.
* pystemd.run now waits for start unit job to finish, before even thinking in
  tearing down the unit (and closing pty's)

0.5.0
=====
* Add `StandardInputData`, `TemporaryFileSystem`, `RuntimeMaxSec`,
   `WatchdogUSec` and `WatchdogSec` to unit definition, so they can be used
   with `pystemd.run`.
* `pystemd.run` always returns a unit.
* `Delegate` and `JoinsNamespaceOf` are also added to unit definition.
* Fix memory leak in path_encode, dbus termination and call_method.

0.4.0
=====
* Add raise_on_fail to `pystemd.run` to raise a error when unit exit with
  non-zero status.
* change on error when property provided to `dbus.call_method` is not the right
  type, still much work to do here.
* added pystemd.daemon.notify as interface to sd_notify.
* added pystemd.daemon.listen_fds as interface to sd_listen_fds.
* added pystemd.daemon.watchdog_enabled as interface to sd_watchdog_enabled.

0.3.0
=====
* Allow non cython-defined methods to accept regular string instead of bytes.
* Add CODE_OF_CONDUCT.md .

0.2.0
=====
* first public release
