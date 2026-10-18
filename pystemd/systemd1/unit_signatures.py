#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#


from pystemd.dbuslib import apply_signature
from pystemd.systemd1.transient_properties import TRANSIENT_PROPERTY_SIGNATURES
from pystemd.utils import x2char_star

# Conveniences pystemd adds on top of systemd's own properties. Each callable
# takes (name, value) and returns the (name, signature, value) to send, so
# e.g. RuntimeMaxSec=1.5 is sent as RuntimeMaxUSec=1500000.
CONVENIENCE_PROPERTIES = {
    b"RuntimeMaxSec": lambda _, value: (b"RuntimeMaxUSec", b"t", int(value * 10**6)),
    b"WatchdogSec": lambda _, value: (b"WatchdogUSec", b"t", int(value * 10**6)),
    b"TimeoutStopSec": lambda _, value: (
        b"TimeoutStopUSec",
        b"t",
        int(value * 10**6),
    ),
    b"TimeoutStartSec": lambda _, value: (
        b"TimeoutStartUSec",
        b"t",
        int(value * 10**6),
    ),
    b"RestartSec": lambda _, value: (b"RestartUSec", b"t", int(value * 10**6)),
    b"CPUQuota": lambda _, value: (b"CPUQuotaPerSecUSec", b"t", int(value * 10**6)),
    b"ListenStream": lambda _, value: (b"Listen", b"a(ss)", [(b"Stream", value)]),
    b"ListenDatagram": lambda _, value: (b"Listen", b"a(ss)", [(b"Datagram", value)]),
    b"ListenSequentialPacket": lambda _, value: (
        b"Listen",
        b"a(ss)",
        [(b"SequentialPacket", value)],
    ),
    b"ListenNetlink": lambda _, value: (b"Listen", b"a(ss)", [(b"Netlink", value)]),
    b"ListenSpecial": lambda _, value: (b"Listen", b"a(ss)", [(b"Special", value)]),
    b"ListenMessageQueue": lambda _, value: (
        b"Listen",
        b"a(ss)",
        [(b"MessageQueue", value)],
    ),
    b"ListenFIFO": lambda _, value: (b"Listen", b"a(ss)", [(b"FIFO", value)]),
    b"ListenUSBFunction": lambda _, value: (
        b"Listen",
        b"a(ss)",
        [(b"USBFunction", value)],
    ),
    # Escape hatch: the value is the (name, signature, value) tuple to send.
    b"_custom": lambda _, value: value,
}

# Property name -> either a signature, or a callable as described above.
KNOWN_UNIT_SIGNATURES = {**TRANSIENT_PROPERTY_SIGNATURES, **CONVENIENCE_PROPERTIES}


def signature_array(properties):
    args = [(ord(b"a"), b"(sv)")]
    # pyrefly: ignore [bad-assignment]
    for prop_name, prop_value in properties.items():
        prop_name = x2char_star(prop_name)
        signature = KNOWN_UNIT_SIGNATURES[prop_name]

        if callable(signature):
            prop_name, signature, prop_value = signature(prop_name, prop_value)

        args += [(ord(b"r"), b"sv"), (ord(b"s"), prop_name)]
        args += [(ord(b"v"), signature)]
        args += apply_signature(signature, [prop_value])
        args += [(-1, None), (-1, None)]
    args += [(-1, None)]

    return args
