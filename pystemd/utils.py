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

import six


def x2char_star(what_to_convert):
    """
    converts `what_to_convert` to whatever the platform understand as char*,
    for python2 this is if unicode we turn it into a string, and if this is
    python3 and what you pass is a str we convert it into bytes
    """

    if isinstance(what_to_convert, six.text_type):
        return what_to_convert.encode()
    return what_to_convert
