#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from pystemd.base import SDObject


class Manager(SDObject):
    def __init__(self, bus=None, _autoload=False):
        super(Manager, self).__init__(
            destination=b"org.freedesktop.machine1",
            path=b"/org/freedesktop/machine1",
            bus=bus,
            _autoload=_autoload,
        )
