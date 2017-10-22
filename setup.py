#
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


__version__ = '0.1.0'

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()


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
    packages=['pystemd'],
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
    long_description=long_description,
    license='BSD'
)
