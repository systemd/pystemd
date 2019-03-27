# pystemd.journal

This just provides a Python interface to some common journal operations, for
complex stuff i would still recommend go and use [python-systemd](https://github.com/systemd/python-systemd)
but if the method below serve your needs, and you are already using pystemd...
go for it!!!

Usage
-----

To send a message to the journal use `pystemd.journal.log`, you just need to specify a `priority`
and a message, but you can provide extra info

Send a `message` to the journal with the `priority` specified
examples:

```python
import logging
import pystemd.journal

pystemd.journal.log(
  logging.INFO,
  "everything is awesome",
  SYSLOG_IDENTIFIER="tegan"
)
```

will result in the following message

```json

{

  "SYSLOG_IDENTIFIER" : "tegan",
  "PRIORITY" : "20",
  "MESSAGE" : "everything is awesome",


  "_AUDIT_LOGINUID" : "119482",
  "_MACHINE_ID" : "2b55b0f0b3b245b38020cb1465b4b754",
  "_EXE" : "/usr/local/bin/python3.6",
  "_SYSTEMD_OWNER_UID" : "119482",
  "CODE_CONTEXT" : "['    SYSLOG_IDENTIFIER=\"tegan\"\\n']",
  "_AUDIT_SESSION" : "84702",
  "CODE_FILE" : [
          "/libs/pystemd/pystemd-cython-lib=pystemd/journal.cpp/pystemd/journal.cpp",
          "/home/aleivag/myapp"
  ],
  "__MONOTONIC_TIMESTAMP" : "6193682365668",
  "_SYSTEMD_UNIT" : "session-84701.scope",
  "_SYSTEMD_SESSION" : "84701",
  "_CAP_EFFECTIVE" : "0",
  "_HOSTNAME" : "aleivag.myhome.cl",
  "_SELINUX_CONTEXT" : "user_u:base_r:base_t",
  "_SYSTEMD_USER_UNIT" : "init.scope",
  "__REALTIME_TIMESTAMP" : "1553620120462027",
  "_UID" : "119482",
  "_COMM" : "python3.6",
  "CODE_FUNC" : [
          "<module>",
          "__pyx_pf_7pystemd_7journal_sendv"
  ],
  "_BOOT_ID" : "bb62f75ca48b4814802150d624c0e4df",
  "_PID" : "2078439",
  "_GID" : "100",
  "__CURSOR" : "s=16f07e48a19b4993a5593d58197f904c;i=1bae8925;b=bb62f75ca48b4814802150d624c0e4df;m=5a2143cbce4;t=585025f6562cb;x=9ef5c1d295402e55",
  "_SYSTEMD_INVOCATION_ID" : "c95f2d49f9f44eb4ac67e50302871eb6",
  "_TRANSPORT" : "journal",
  "CODE_LINE" : [
          "4",
          "1722"
  ],
  "_SYSTEMD_USER_SLICE" : "-.slice",
  "_CMDLINE" : "/home/aleivag/myapp",
  "_SYSTEMD_CGROUP" : "/user.slice/user-119482.slice/session-84701.scope/init.scope",
  "_SOURCE_REALTIME_TIMESTAMP" : "1553620120461937",
  "_SYSTEMD_SLICE" : "user-119482.slice"
}

```

If you know what you are doing, you can use `pystemd.journal.sendv` to send custom
information, like:

```python
import logging
import pystemd.journal

pystemd.journal.sendv(
  f"PRIORITY={logging.INFO}",
  MESSAGE="everything is awesome",
  SYSLOG_IDENTIFIER="tegan"
)
```

`pystemd.journal.sendv` will allow you to pass fields to the journal in 2 forms,
one is by you writing the key and value in text form, like:

```python
import logging
import pystemd.journal

pystemd.journal.sendv(
  f"PRIORITY={logging.INFO}",
  "MESSAGE=everything is awesome",
  "SYSLOG_IDENTIFIER=tegan",
)
```

or by key arguments


```python
import logging
import pystemd.journal

pystemd.journal.sendv(
  PRIORITY=logging.INFO,
  MESSAGE="everything is awesome",
  SYSLOG_IDENTIFIER="tegan",
)
```

and combining this 2 options like the first example:

```python
pystemd.journal.sendv(
  f"PRIORITY={logging.INFO}",  #  arg will be passed as is.
  MESSAGE="everything is awesome",  #  kwarg, will be converted to key=val.
  SYSLOG_IDENTIFIER="tegan"
)

```
