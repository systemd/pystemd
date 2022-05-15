#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Any, Iterable, List, Tuple, Union

def x2char_star(what_to_convert: Any, convert_all: bool = False) -> bytes: ...
def str2cmd(
    cmd: Union[str, bytes], cont: bool = False
) -> Tuple[bytes, Tuple[bytes, ...], bool]: ...
def strlist2cmd(
    strlist: Iterable[Union[str, bytes]], cont: bool = False
) -> Tuple[bytes, Tuple[bytes, ...], bool]: ...
def x2cmdlist(
    what_to_convert: Any, cont: bool = False
) -> List[Tuple[bytes, Tuple[bytes, ...], bool]]: ...
