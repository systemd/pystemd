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

import runpy
import sys
from pathlib import Path

import pystemd
import pystemd.daemon
import pystemd.journal
import pystemd.run
# pyrefly: ignore [missing-import]
from IPython.terminal.embed import InteractiveShellEmbed

display_banner = """
Welcome to pystemd  {pystemd.__version__} interactive shell for python {sys.version}.
""".format(pystemd=pystemd, sys=sys)


def shell() -> None:
    shell = InteractiveShellEmbed()
    shell.show_banner(display_banner)
    shell.mainloop()


def main(mod: Path) -> None:
    # pyrefly: ignore [bad-argument-type]
    runpy.run_path(mod, {}, "__main__")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(Path(__file__).resolve().absolute().parent / sys.argv[1])
    else:
        shell()
