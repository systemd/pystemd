#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

"""
This is a set of example of stuff you could do with a SDManager object
"""

from pystemd.manager import SDManager


def list_units() -> None:
    with SDManager() as manager:
        print("Version", manager.Manager.Version)
        print("Architecture", manager.Manager.Architecture)

        # List Units
        for unit, state in manager.Manager.ListUnitFiles():
            print("    {} is {}".format(unit, state))
