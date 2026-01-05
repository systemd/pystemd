#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#


import glob
import subprocess
import sys
from pathlib import Path

from setuptools import setup
from setuptools.extension import Extension

compile_time_env = {"LIBSYSTEMD_VERSION": 500}

try:
    compile_time_env["LIBSYSTEMD_VERSION"] = int(
        subprocess.check_output(["pkg-config", "--modversion", "libsystemd"])
    )
    # Extension has no means to interrogate pkg-config: https://bugs.python.org/issue28207#msg277413
except FileNotFoundError:
    sys.exit(
        '"pkg-config" command could not be found. Please ensure "pkg-config" is installed into your PATH.'
    )
except subprocess.CalledProcessError as e:
    sys.exit(
        "`%s` failed. Please ensure all prerequisite packages from README.md are installed."
        % " ".join(e.cmd)
    )
except ValueError:
    sys.exit("libsystemd version returned by pkg-config is not a plain integer!")

# Use C extensions if respective files are present. Else let Cython modules be
# compiled to C code. The latter is the case when using a clone of the git
# repository, unlike the source distribution which includes both .pyx and .c
# files.
if glob.glob("pystemd/*.c"):
    external_modules = [
        Extension(cext[:-2].replace("/", "."), [cext], libraries=["systemd"])
        for cext in glob.glob("pystemd/*.c")
    ]
else:
    try:
        from Cython.Build import cythonize

        external_modules = cythonize(
            [Extension("*", ["pystemd/*.pyx"], libraries=["systemd"])],
            compile_time_env=compile_time_env,
        )
    except (ImportError, ModuleNotFoundError):
        # If we're just asking for the version, we don't actually need Cython
        if len(sys.argv) == 2 and sys.argv[1] == "--version":
            external_modules = []
            pass
        else:
            raise RuntimeError("Cython not installed.")


setup(
    name="pystemd",
    version="0.15.1",
    author="Alvaro Leiva Geisse",
    author_email="aleivag@gmail.com",
    packages=["pystemd", "pystemd.systemd1", "pystemd.machine1", "pystemd.DBus"],
    ext_modules=external_modules,
    package_data={
        "pystemd": [
            str(p.relative_to("pystemd")) for p in Path("pystemd").glob("**/*.pyi")
        ]
    },
    install_requires=[
        "lxml",
        "psutil",
    ],
    description="A systemd binding for python",
)
