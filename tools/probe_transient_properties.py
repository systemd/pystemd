#!/usr/bin/env python3
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

"""Ask a running systemd which properties StartTransientUnit accepts, and with
which D-Bus signature.

The signature systemd accepts when *setting* a property is often not the type
the introspection XML reports for *reading* it (ExecStart is read as
a(sasbttttuii) but set as a(sasb)), and some properties are write-only
(OnCalendar, MemoryMaxScale). systemd does not publish the set signatures
anywhere, so this tool measures them.

Every candidate is sent as a single-property StartTransientUnit call with an
empty/zero value. systemd checks the property name before it reads the value,
and reads the value before validating it, so:

  "Cannot set property X, or unknown property."  -> name unknown for type
  same answer as for a sentinel type nothing reads -> signature rejected
  any other answer                               -> signature accepted

A known name that accepts no signature is "ignored" when the sentinel gets
the same answer as setting no property at all (systemd skips the value, as
it does for removed cgroup v1 settings), and "refused" otherwise.

Candidate names and signatures come from the machine itself: the
introspection XML, the unit file directives systemd knows, and the string
literals in libsystemd-core.

This creates (and immediately stops) transient units, so run it as root in a
throwaway container or VM, never on a machine you care about:

    python3 tools/probe_transient_properties.py OUTPUT.json
"""

from __future__ import annotations

import contextlib
import glob
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from pystemd.dbuslib import DBus

# swap units cannot be created transiently.
UNIT_TYPES = [
    "service",
    "socket",
    "timer",
    "path",
    "mount",
    "automount",
    "slice",
    "scope",
]
UNKNOWN = "or unknown property"
SENTINEL = "(yyyyyyyyyyyyyyyy)"  # a type no setter reads
BASIC = "ybnqiuxtdsogh"
INTERFACES = "/usr/share/dbus-1/interfaces"


def split_complete(sig):
    """Split a signature into its complete types; ValueError if malformed."""
    out, i = [], 0
    while i < len(sig):
        j = _complete_type_end(sig, i)
        out.append(sig[i:j])
        i = j
    return out


def _complete_type_end(sig, i):
    c = sig[i]
    if c in BASIC or c == "v":
        return i + 1
    if c == "a":
        if i + 1 >= len(sig):
            raise ValueError(sig)
        if sig[i + 1] == "{":
            k = _complete_type_end(sig, i + 2)
            if sig[k - 1] not in BASIC:
                raise ValueError(sig)
            v = _complete_type_end(sig, k)
            if v >= len(sig) or sig[v] != "}":
                raise ValueError(sig)
            return v + 1
        return _complete_type_end(sig, i + 1)
    if c == "(":
        j = i + 1
        if j < len(sig) and sig[j] == ")":
            raise ValueError(sig)
        while j < len(sig) and sig[j] != ")":
            j = _complete_type_end(sig, j)
        if j >= len(sig):
            raise ValueError(sig)
        return j + 1
    raise ValueError(sig)


def is_single_type(sig):
    try:
        return len(split_complete(sig)) == 1
    except (ValueError, IndexError):
        return False


def struct_prefixes(sig):
    """a(sasbttttuii) -> a(sasb), a(sasbt), ..., a(s), a(as), ...

    Setters often take a leading part of the struct the getter returns."""
    out = set()
    if sig.startswith("a("):
        body, wrap = sig[2:-1], "a{}"
    elif sig.startswith("("):
        body, wrap = sig[1:-1], "{}"
    else:
        return out
    try:
        parts = split_complete(body)
    except (ValueError, IndexError):
        return out
    for n in range(1, len(parts)):
        out.add(wrap.format("(" + "".join(parts[:n]) + ")"))
    for p in parts:
        out.add(wrap.format(p))
    return out


def zero_value(sig, fd):
    """pystemd dbuslib argument stream for an empty/zero value of sig."""
    c = sig[0]
    if c in "ybnqiuxt":
        return [(ord(c), 0)]
    if c == "d":
        return [(ord(c), 0.0)]
    if c in "sg":
        return [(ord(c), b"")]
    if c == "o":
        return [(ord(c), b"/")]
    if c == "h":
        return [(ord(c), fd)]
    if c == "v":
        return [(ord("v"), b"s"), (ord("s"), b""), (-1, None)]
    if c == "a":
        return [(ord("a"), sig[1:].encode()), (-1, None)]
    if c == "(":
        out = [(ord("r"), sig[1:-1].encode())]
        for p in split_complete(sig[1:-1]):
            out += zero_value(p, fd)
        return out + [(-1, None)]
    raise ValueError(sig)


def xml_read_types():
    types = {}
    for f in glob.glob(f"{INTERFACES}/org.freedesktop.systemd1.*.xml"):
        for p in ET.parse(f).getroot().iter("property"):
            types.setdefault(p.get("name"), set()).add(p.get("type"))
    return types


def xml_all_types():
    out = set()
    for f in glob.glob(f"{INTERFACES}/*.xml"):
        for el in ET.parse(f).getroot().iter():
            if el.tag in ("property", "arg") and el.get("type"):
                out.add(el.get("type"))
    return out


def core_literals():
    lib = min(
        glob.glob("/usr/lib/*/systemd/libsystemd-core-*.so")
        + glob.glob("/usr/lib/systemd/libsystemd-core-*.so")
    )
    with open(lib, "rb") as f:
        found = {s.decode() for s in re.findall(rb"[\x20-\x7e]{1,80}", f.read())}
    # The linker merges a literal into a longer one it is a suffix of
    # ("MemoryLowScale" lives inside "DefaultMemoryLowScale", "(st)" inside
    # "a(st)"), so suffixes of every literal are candidates as well.
    return {s[i:] for s in found for i in range(len(s))}


def unit_file_directives():
    out = subprocess.run(
        ["/usr/lib/systemd/systemd", "--dump-configuration-items"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return {
        line.split("=", 1)[0]
        for line in out.splitlines()
        if "=" in line and not line.startswith(("[", "#"))
    }


def canonical(accepted, read_types):
    """Pick one signature for a property systemd accepts several for."""
    if len(accepted) == 1:
        return next(iter(accepted))
    if accepted & read_types:
        (sig,) = accepted & read_types
        return sig
    # sd-bus reads string arrays from any of as/ao/ag.
    as_strings = {re.sub("[og]", "s", s) for s in accepted}
    if len(as_strings) == 1 and as_strings <= accepted:
        return next(iter(as_strings))
    raise RuntimeError(f"ambiguous signatures {sorted(accepted)}")


class Prober:
    def __init__(self):
        self.bus = DBus()
        self.bus.open()
        self.fd = os.open("/dev/null", os.O_RDONLY)
        self.n = 0
        self.calls = 0

    def _manager(self, method, args):
        return self.bus.call_method(
            b"org.freedesktop.systemd1",
            b"/org/freedesktop/systemd1",
            b"org.freedesktop.systemd1.Manager",
            method,
            args,
        )

    def answer(self, unit_type, name=None, sig=None):
        """systemd's answer to setting name to a zero value of type sig, or
        to setting no property at all."""
        self.n += 1
        self.calls += 1
        unit = f"probe{self.n}.{unit_type}".encode()
        prop = []
        if name is not None:
            prop = [
                (ord("r"), b"sv"),
                (ord("s"), name.encode()),
                (ord("v"), sig.encode()),
                *zero_value(sig, self.fd),
                (-1, None),
                (-1, None),
            ]
        args = [
            (ord("s"), unit),
            (ord("s"), b"fail"),
            (ord("a"), b"(sv)"),
            *prop,
            (-1, None),
            (ord("a"), b"(sa(sv))"),
            (-1, None),
        ]
        try:
            self._manager(b"StartTransientUnit", args)
        except Exception as e:  # noqa: BLE001
            msg = getattr(e, "err_message", None) or str(e)
            msg = msg.decode() if isinstance(msg, bytes) else str(msg)
            return re.sub(r"probe\d+", "UNIT", msg)
        # The unit started; stopping it is best effort.
        with contextlib.suppress(Exception):
            self._manager(b"StopUnit", [(ord("s"), unit), (ord("s"), b"replace")])
        return "ok"


def probe(log=print):
    read_types = xml_read_types()
    literals = core_literals()

    names = (
        set(read_types)
        | unit_file_directives()
        | {s for s in literals if re.fullmatch(r"[A-Z][A-Za-z0-9]{2,63}", s)}
    )

    sigs = set(xml_all_types())
    for s in literals:
        if len(s) <= 40 and is_single_type(s):
            sigs.add(s)
            if s.startswith("("):
                sigs.add("a" + s)
    for s in list(sigs):
        sigs |= struct_prefixes(s)
    sigs = {s for s in sigs if is_single_type(s)} - {SENTINEL}

    prober = Prober()
    accepted = {}  # name -> set of signatures
    refused = {}  # name -> reason, for names known but never accepted
    ignored = set()  # names whose value systemd skips without reading
    unit_types = {}

    for unit_type in UNIT_TYPES:
        settable = []
        baseline = prober.answer(unit_type)
        for name in sorted(names):
            sentinel = prober.answer(unit_type, name, SENTINEL)
            if UNKNOWN in sentinel:
                continue
            ok = {
                sig for sig in sigs if prober.answer(unit_type, name, sig) != sentinel
            }
            if ok:
                settable.append(name)
                if accepted.setdefault(name, ok) != ok:
                    raise RuntimeError(f"{name}: signatures differ by unit type")
            elif sentinel == baseline:
                ignored.add(name)
            else:
                refused.setdefault(name, sentinel)
        unit_types[unit_type] = settable
        subprocess.run(["systemctl", "reset-failed"], check=False)
        log(f"{unit_type}: {len(settable)} settable, {prober.calls} calls")

    for name in accepted:
        refused.pop(name, None)
        ignored.discard(name)
    for name in ignored:
        refused.pop(name, None)

    version = subprocess.run(
        ["systemctl", "--version"], capture_output=True, text=True, check=True
    ).stdout.splitlines()[0]

    return {
        "systemd": version,
        "properties": {
            name: canonical(ok, read_types.get(name, set()))
            for name, ok in sorted(accepted.items())
        },
        "unit_types": unit_types,
        "ignored": sorted(ignored),
        "refused": dict(sorted(refused.items())),
    }


def main():
    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} OUTPUT.json")
    result = probe(log=lambda m: print(m, file=sys.stderr, flush=True))
    with open(sys.argv[1], "w") as f:
        json.dump(result, f, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()
