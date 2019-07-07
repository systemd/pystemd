# cython: language_level=3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

# This header includes only the symbols from the v237+ releases of systemd:
# https://raw.githubusercontent.com/systemd/systemd/v237/NEWS

cdef extern from "systemd/sd-bus.h":
  int sd_bus_match_signal(
    sd_bus *bus,
    sd_bus_slot **ret,
    const char *sender,
    const char *path,
    const char *interface,
    const char *member,
    sd_bus_message_handler_t callback,
    void *userdata
  )
