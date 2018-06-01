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

import os
import sys

__version__ = "0.5"

_endstr = ".dev"

release_file = os.path.join(os.path.dirname(__file__), "RELEASE")
if os.path.exists(release_file):
    with open(release_file) as release_fileobj:
        _endstr = ".{}".format(release_fileobj.read().strip())

__version__ += _endstr

sys.modules[__name__] = __version__
