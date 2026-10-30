#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

"""
Helpers used across pystemd. Everything that used to live in the
pystemd/utils.py module is re-exported here, so `from pystemd.utils import
x2char_star` (and friends) keeps working.
"""

from pystemd.utils.ns import join_namespaces
from pystemd.utils.typing import T, unwrap
from pystemd.utils.unit import random_unit_name
from pystemd.utils.x2 import str2cmd, strlist2cmd, x2char_star, x2cmdlist

__all__ = [
    "T",
    "join_namespaces",
    "random_unit_name",
    "str2cmd",
    "strlist2cmd",
    "unwrap",
    "x2char_star",
    "x2cmdlist",
]
