#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#

"""
This file is here so we can annotate a few example of usage, and also it turns
into a nice ipython shell, to run commands interactively.

Needless to say that you need to have the ipython installed.
"""

import sys

import pystemd
from IPython.terminal.embed import InteractiveShellEmbed


display_banner = """
Welcome to pystemd  {pystemd.__version__} interactive shell for python {sys.version}.
""".format(
    pystemd=pystemd, sys=sys
)

if __name__ == "__main__":
    shell = InteractiveShellEmbed()
    shell.show_banner(display_banner)
    shell.mainloop()
