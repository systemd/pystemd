Changelog
---------

We annotate all changes here, keep in mind that the high version may not be
the one you find pypi, but its the one in development.

dev
=====
* Fix `pystemd.run(wait=True)` / `wait_for_activation=True` hanging forever on hosts where no other client is subscribed to systemd signals
* Fix `pystemd.run` missing unit state changes when several D-Bus signals arrive at once
* Fix `pystemd.futures` on Python 3.14+, where the default multiprocessing start method is no longer fork
* Fix `pystemd.futures` ignoring `User=` on systemd >= 255
* Fix `pystemd.futures.TransientUnitPoolExecutor` leaking its unit when the parent process is killed
* Add `PrivatePIDs`, `ProtectHostnameEx` and `SystemCallErrorNumber` to systemd1 KNOWN_UNIT_SIGNATURES
* Fix `pystemd.run(wait_for_activation=True)` hanging forever when the unit fails to start
* Add `FileDescriptorStoreMax` and `FileDescriptorStorePreserve` to systemd1 KNOWN_UNIT_SIGNATURES
* Add `fds=` to `pystemd.daemon.notify` (sd_pid_notify_with_fds) and add `pystemd.daemon.listen_fds_with_names` (file descriptor store / named socket activation)
* Add `pystemd.daemon.store_fd` and `pystemd.daemon.store_fds` helpers for the file descriptor store
* Split `pystemd.utils` into a package (`pystemd.utils.{x2,unit,typing}`); existing imports keep working
* Add `pystemd.utils.ns.join_namespaces` (atomic pidfd `setns`, with a per-namespace fallback); `pystemd.futures` uses it, which also fixes leaking one fd per namespace in every worker
* Add `delegate=` to `pystemd.run`, a shortcut for `extra={"Delegate": ...}`
* Add `OOMPolicy`, `OOMScoreAdjust` and the `ManagedOOM*` properties to systemd1 KNOWN_UNIT_SIGNATURES

0.15.3
=====
* Fix type invariance causing too strict typing

0.15.2
=====
* Add E2E testing infrastructure using mkosi for running tests in a real systemd environment
* Improve type annotations throughout pystemd, modernizing to Python 3.10+ syntax
* Add AmbientCapabilities to systemd1 KNOWN_UNIT_SIGNATURES
* Improve README.md clarity, spelling, and grammar

0.15.1
=====
* Add `wait_for_activation` parameter to pystemd.run to wait only for service activation without blocking until completion
* Document `cwd` and `wait_for_activation` parameters in pystemd.run

0.15.0
=====
* Drop support for Python 3.6-3.10, now requires Python 3.11+
* Add `unit` property and `unit_name` to TransientUnitProcess for easy access to the running unit
* Change development tooling to use uv for package management
* Change lint/format stack from black/mypy to ruff/pyrefly
* Add a lot of typing

0.14.0
=====
* allow SDObject and Unit to be pickled

0.13.4
=====
* add apt-get update to release

0.13.3
=====
* Fix deprecation warning: LICENSE is autodetected
* fixing DbusRemote
* enable user_mode in futures

0.13.2
=====
* selecting all .pyi files

0.13.1
=====
* fix setup.py

0.13.0
=====
* adding coverage information
* changes tests to pystes
* adding support for pyproject.toml
* adding extra properties for unit 

0.12.0
=====
* initial support for pystemd.futures

0.11.0
=====
* native support for stop_cmd, (pre|post)_start_cmd and post_stop_cmd in pystemd.run.
* adding lxml as a dependency.
* drop support for python 3.4 and 3.5 (yey welcome f-strings)
* change using select.select to use DefaultSelector in pystemd.run

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
