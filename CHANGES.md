Changelog
---------

We annotate all changes here, keep in mind that the high version may not be
the one you find pypi, but its the one in development.

0.7.0
=====
* Modify README to show the right systemd min version.
* Added `pystemd.journal` with methods `log` and `sendv`.
* Added `booted` support in `pystemd.daemon` to know if a system was booted with
  systemd.
* allow None (translated to NULL) options in DBUS.match_signal.
* Added `address` option to `pystemd.run` to support custom dbus addresses.

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
