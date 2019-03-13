#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#


import ast
import atexit
import glob
import os
import sys
import time
from pathlib import Path

import _ast
from setuptools import setup
from setuptools.extension import Extension


THIS_DIR = Path(__file__).parent

long_description = (THIS_DIR / "README.md").read_text()

# get and compute the version string
version_file = THIS_DIR / "pystemd" / "__version__.py"
release_file = THIS_DIR / "pystemd" / "RELEASE"

parsed_file = ast.parse(version_file.read_text())
__version__ = [
    expr.value.s
    for expr in parsed_file.body
    if isinstance(expr, _ast.Assign)
    and isinstance(expr.targets[0], _ast.Name)
    and isinstance(expr.value, _ast.Str)
    and expr.targets[0].id == "__version__"
][0]

release_tag = "{}".format(int(time.time()))


if release_file.exists():
    __version__ += ".0"
elif "sdist" in sys.argv:
    with open(release_file, "w") as release_fileobj:
        atexit.register(lambda *x: os.remove(release_file))
        release_fileobj.write(release_tag)
    __version__ += ".0"
else:
    __version__ += ".{}".format(release_tag)


# If you are installing a clone of the repo, you should always compile the pyx
# files into c code. since we never include the c files in the git repo.
# But if you are installing this from a source distribution, then we dont pack
# the pyx files, but we do pack the c extensions, so you need to use that.
if glob.glob("pystemd/*.pyx"):
    from Cython.Build import cythonize

    external_modules = cythonize(
        [Extension("*", ["pystemd/*.pyx"], libraries=["systemd"])]
    )
else:
    external_modules = [
        Extension(cext[:-2].replace("/", "."), [cext], libraries=["systemd"])
        for cext in glob.glob("pystemd/*.c")
    ]


setup(
    name="pystemd",
    version=__version__,
    packages=["pystemd", "pystemd.systemd1", "pystemd.machine1", "pystemd.DBus"],
    author="Alvaro Leiva",
    author_email="aleivag@fb.com",
    ext_modules=external_modules,
    url="https://github.com/facebookincubator/pystemd",
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
    ],
    keywords=["systemd"],
    description="A systemd binding for python",
    package_data={"pystemd": ["RELEASE"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="LGPL-2.1+",
)
