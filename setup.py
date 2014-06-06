#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: setup
# Created: 27.12.2010
# License: MIT license
#
#    Copyright (C) 2010  Manfred Moitzi
#

import os
from distutils.core import setup

from version import VERSION

AUTHOR_NAME = 'Manfred Moitzi'
AUTHOR_EMAIL = 'mozman@gmx.at'

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '%s' not found.\n" % fname

setup(name='ezodf',
    version=VERSION,
    description='A Python package to create/manipulate OpenDocumentFormat files.',
    author=AUTHOR_NAME,
    url='http://bitbucket.org/mozman/ezodf',
    download_url='http://bitbucket.org/mozman/ezodf/downloads',
    author_email=AUTHOR_EMAIL,
    packages=['ezodf'],
    provides=['ezodf'],
    install_requires=['lxml'],
    keywords=['ODF', 'OpenDocumentFormat', 'OpenOffice', 'LibreOffice'],
    long_description=read('README.rst')+read('NEWS.rst'),
    platforms="OS Independent",
    license="MIT License",
    classifiers=[
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Office/Business :: Office Suites",
    ]
     )
