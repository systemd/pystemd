#!/usr/bin/env python3
#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree.
#


import ast
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

THIS_DIR = Path(__file__).parent

with (THIS_DIR / "README.md").open() as f:
    long_description = f.read()

# get and compute the version string
version_file = THIS_DIR / "pystemd" / "__version__.py"
with version_file.open() as f:
    parsed_file = ast.parse(f.read())

__version__ = [
    expr.value.s
    for expr in parsed_file.body
    if isinstance(expr, ast.Assign)
    and isinstance(expr.targets[0], ast.Name)
    and isinstance(expr.value, ast.Str)
    and expr.targets[0].id == "__version__"
][0]

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

package_data = []
package_data.extend(glob.glob("pystemd/*.pyi"))
package_data.extend(glob.glob("pystemd/*/*.pyi"))

setup(
    name="pystemd",
    version=__version__,
    packages=["pystemd", "pystemd.systemd1", "pystemd.machine1", "pystemd.DBus"],
    author="Alvaro Leiva",
    author_email="aleivag@meta.com",
    ext_modules=external_modules,
    url="https://github.com/facebookincubator/pystemd",
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
    ],
    keywords=["systemd"],
    description="A systemd binding for python",
    package_data={
        "pystemd": [str(Path(p).relative_to("pystemd")) for p in package_data]
    },
    install_requires=[
        "lxml",
        "psutil",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="LGPL-2.1+",
)
