# cython: language_level=3
#
# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

cimport pystemd.dbusc as dbusc

import inspect

from pystemd.utils import x2char_star
from libc.stdlib cimport malloc, free


def sendv(*args, **kwargs):
  """
  send lines directly to the journal.

example:

```python
import logging
import pystemd.journal

pystemd.journal.sendv(
  f"PRIORITY={logging.INFO}",
  MESSAGE="everything is awesome",
  SYSLOG_IDENTIFIER="tegan"
)
```

  """
  cdef:
    char * text
    int le
    bytes i_str
    dbusc.iovec * iov

  all_options = [
    x2char_star(i)
    for i in args
  ] + [
    b"=".join([x2char_star(key), x2char_star(val, convert_all=True)])
    for key, val in kwargs.items()
  ]

  le = len(all_options)
  iov = <dbusc.iovec *> malloc(le * sizeof(dbusc.iovec))


  for i, iv in enumerate(all_options):
    i_str = iv
    text = i_str
    iov[i].iov_base = text
    iov[i].iov_len = len(text)

  dbusc.sd_journal_sendv(iov, len(all_options))

  free(iov)

def log(int priority, message, **kwargs):
  """
  Send a `message` to the journal with the `priority` specified
  examples:

  ```python
import logging
import pystemd.journal

pystemd.journal.log(
  logging.INFO,
  "everything is awesome",
  SYSLOG_IDENTIFIER="tegan"
)
  ```
  """

  stack = inspect.stack()[0]


  CODE_FILE = stack[1]
  CODE_LINE = stack[2]
  CODE_FUNC = stack[3]
  CODE_CONTEXT = stack[4]

  sendv(
    MESSAGE=x2char_star(message),
    PRIORITY=priority,
    CODE_FILE=CODE_FILE,
    CODE_LINE=CODE_LINE,
    CODE_FUNC=CODE_FUNC,
    CODE_CONTEXT=CODE_CONTEXT,
    **kwargs
  )
