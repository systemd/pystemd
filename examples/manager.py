#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

"""
This is a set of example of stuff you could do with a SDManager object
"""

from pystemd.manager import SDManager


def list_units():
    with SDManager() as manager:
        print("Version", manager.Manager.Version)
        print("Architecture", manager.Manager.Architecture)

        # List Units
        for unit, state in manager.Manager.ListUnitFiles():
            print("    {} is {}".format(unit, state))
