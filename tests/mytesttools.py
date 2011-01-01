#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: testing tools
# Created: 30.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import os

def in_XML(source, target):
    for element in source.strip().split():
        if element not in target:
            return False
    return True

def testdatafile(filename):
    return os.path.join(os.path.dirname(__file__), "data", filename)