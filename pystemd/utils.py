#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import shlex
import uuid
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple, TypeVar, Union

T = TypeVar("T")


def x2char_star(what_to_convert: Any, convert_all: bool = False) -> bytes:
    """
    Converts `what_to_convert` to whatever the platform understand as char*.
    For python2, if this is unicode we turn it into a string. If this is
    python3 and what you pass is a `str` we convert it into `bytes`.

    If `convert_all` is passed we will also convert non string types, so `1`
    will be `b'1'` and `True` will be true
    """

    if isinstance(what_to_convert, Path):
        return str(what_to_convert).encode()
    elif isinstance(what_to_convert, bytes):
        return what_to_convert
    elif isinstance(what_to_convert, str):
        return what_to_convert.encode()
    elif convert_all:
        if isinstance(what_to_convert, bool):
            return str(what_to_convert).lower().encode()
        return repr(what_to_convert).encode()
    else:
        return what_to_convert


def str2cmd(
    cmd: Union[str, bytes], cont: bool = False
) -> Tuple[bytes, Tuple[bytes, ...], bool]:
    """
    coverts a string (or bytes) into a cmd list usable by the Exec* family of Unit Signatures, you could do


    pystemd.run(
        cmd=...,
        extra={
            b"ExecReload": [str2cmd("/bin/echo 'there is no reaload'")]
        },
    )

    The cont param is for ignore failure and continue

    """
    cmd = x2char_star(cmd).decode()
    cmdlist = tuple(x2char_star(_) for _ in shlex.split(cmd))

    return (cmdlist[0], cmdlist, cont)


def strlist2cmd(
    strlist: Iterable[Union[str, bytes]], cont: bool = False
) -> Tuple[bytes, Tuple[bytes, ...], bool]:
    """
    coverts a command (an array of strings or bytes) into a cmd list usable by the Exec* family of Unit Signatures, you could do


    pystemd.run(
        cmd=...,
        extra={
            b"ExecReload": [strlist2cmd(["/bin/echo, 'there is no reaload'])]
        },
    )
    The cont param is for ignore failure and continue

    """
    cmdlist = [x2char_star(_) for _ in strlist]
    return (cmdlist[0], tuple(cmdlist), cont)


def x2cmdlist(
    what_to_convert: Any, cont: bool = False
) -> List[Tuple[bytes, Tuple[bytes, ...], bool]]:
    """
    a really overloaded helper to convert most things into a cmd list that can be passed natevly to the Exec* family. it should

    1. for None and [] return []
    2. for a single string like "/bin/foo bar" will return as [(b"/bin/foo", (b"/bin/foo", "bar"), False)]
    3. for a list|set of strings|bytes, it should interpret that as a single command, and it should just return that as [(cmd[0], cmd, False)]
    4. for a list|set of list|set, it should interpret that as multiple command, and it should just return that as [(cmd[0], cmd, False) for each cmd]

    The last argument is what systemd uses to determine if the command can continue if failed.

    """
    if what_to_convert is None:
        return []

    if isinstance(what_to_convert, (str, bytes)):
        return [str2cmd(what_to_convert, cont)]

    if not isinstance(what_to_convert, (list, tuple)):
        return what_to_convert

    # at this point tyhis is either a list or a tuple
    if not len(what_to_convert):
        return []

    # if the first element is a string then we just woll this in a double array
    if isinstance(what_to_convert[0], (str, bytes)):
        return [strlist2cmd(what_to_convert, cont)]

    return [strlist2cmd(_, cont) for _ in what_to_convert]


def unwrap(obj: Optional[T], msg="object was None") -> T:
    if obj is None:
        raise ValueError(msg)
    return obj

def random_unit_name(*, unit_type="service", prefix="pystemd"):
    return f"{prefix}{uuid.uuid4().hex}.{unit_type}"
