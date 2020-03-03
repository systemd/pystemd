# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

from typing import Union

def notify(unset_environment: bool, *args: str, **kwargs: Union[int, str]) -> None: ...
