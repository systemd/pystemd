Changelog
---------

We annotate all changes here, keep in mind that the high version may not be
the one you find pypi, but its the one in development.

0.4.0
=====
* Add raise_on_fail to `pystemd.run` to raise a error when unit exit with
  non-zero status.
* change on error when property probided to `dbus.call_method` is not the right
  type, still much work to do here.

0.3.0
=====
* Allow non cython-defined methods to accept regular string instead of bytes.
* Add CODE_OF_CONDUCT.md .

0.2.0
=====
* first public release
