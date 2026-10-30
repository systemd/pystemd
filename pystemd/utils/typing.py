#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def unwrap(obj: T | None, msg="object was None") -> T:
    if obj is None:
        raise ValueError(msg)
    return obj
