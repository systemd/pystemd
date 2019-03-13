#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from pathlib import Path


def x2char_star(what_to_convert, convert_all=False):
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
