#!/usr/bin/env python
# coding:utf-8
# Author:  mozman
# Purpose: setup
# Created: 27.12.2010
# License: MIT license
#
#    Copyright (C) 2010  Manfred Moitzi
#

import os
from setuptools import setup

from version import VERSION

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '%s' not found.\n" % fname

setup(
    version=VERSION,
    long_description=read('README.rst')+read('NEWS.rst')
)
