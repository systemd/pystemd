#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from __future__ import annotations

import uuid


def random_unit_name(*, unit_type="service", prefix="pystemd"):
    return f"{prefix}{uuid.uuid4().hex}.{unit_type}"
