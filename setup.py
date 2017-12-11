#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

import _ast
import ast
import atexit
import os
import sys
import time

from Cython.Build import cythonize
from setuptools import setup
from setuptools.extension import Extension

THIS_DIR = os.path.dirname(__file__)

with open(os.path.join(THIS_DIR, 'README.md')) as f:
    long_description = f.read()


# get and compute the version string
version_file = os.path.join(THIS_DIR, 'pystemd', '__version__.py')
release_file = os.path.join(THIS_DIR, 'pystemd', 'RELEASE')
with open(version_file) as version:
    parsed_file = ast.parse(version.read())
    __version__ = [
        expr.value.s
        for expr in parsed_file.body
        if isinstance(expr, _ast.Assign)
        and isinstance(expr.targets[0], _ast.Name)
        and isinstance(expr.value, _ast.Str)
        and expr.targets[0].id == '__version__'
    ][0]

    release_tag = '{}'.format(int(time.time()))


if os.path.exists(release_file):
    __version__ += '.0'
elif 'sdist' in sys.argv:
    with open(release_file, 'w') as release_fileobj:
        atexit.register(lambda *x: os.remove(release_file))
        release_fileobj.write(release_tag)
    __version__ += '.0'
else:
    __version__ += '.{}'.format(release_tag)

# TODO: change this to use the c files instead of pyx if availables
# on normal setup, or use the pyx in dev mode. also maybe generate cpp instead
# of regular c.

cython_ext = cythonize([
    Extension(
        "*", ["pystemd/*.pyx"],
        libraries=['systemd']),
])

setup(
    name='pystemd',
    version=__version__,
    packages=['pystemd', 'pystemd.systemd1', 'pystemd.machine1'],
    author='Alvaro Leiva',
    author_email='aleivag@fb.com',
    ext_modules=cython_ext,
    url='https://github.com/facebookincubator/pystemd',
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    keywords=['systemd'],
    description='A systemd binding for python',
    install_requires=['six'],
    package_data={'pystemd': ['RELEASE']},
    long_description=long_description,
    license='BSD'
)
