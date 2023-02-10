#
# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

import re
from contextlib import contextmanager
from typing import Any, AnyStr, Iterator, Optional
from xml.dom.minidom import Element

from pystemd.dbuslib import apply_signature, DBus
from pystemd.utils import x2char_star

class SDObject(object):
    def __init__(
        self,
        destination: AnyStr,
        path: AnyStr,
        bus=Optional[DBus],
        _autoload: bool = False,
    ) -> None: ...
    def __enter__(self) -> SDObject: ...
    @contextmanager
    def bus_context(self) -> Iterator[DBus]: ...
    def get_introspect_xml(self) -> Element: ...
    def load(self, force: bool = False) -> None: ...

class SDInterface(object):
    def __init__(self, sd_object: SDObject, interface_name: AnyStr) -> None: ...
    def __repr__(self) -> str: ...
    def _get_property(self, property_name: str) -> Any: ...
    def _set_property(self, property_name: AnyStr, value: Any) -> None: ...
