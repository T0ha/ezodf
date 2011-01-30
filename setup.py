#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: setup
# Created: 27.12.2010
#
#    Copyright (C) 2010  Manfred Moitzi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from distutils.core import setup

VERSION = '0.2.1'
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
    requires=['lxml'],
    keywords=['ODF', 'OpenDocumentFormat', 'OpenOffice', 'LibreOffice'],
    long_description=read('README.txt')+read('NEWS.txt'),
    platforms="OS Independent",
    license="GPLv3",
    classifiers=[
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.1",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Office/Business :: Office Suites",
    ]
     )
