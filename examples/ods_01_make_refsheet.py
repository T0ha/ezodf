#!/usr/bin/env python
#coding:utf-8
# Purpose: example make_refshett.py
# Created: 05.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

import ezodf

NCOLS=10
NROWS=10

ods = ezodf.newdoc('ods', 'refsheet.ods')

sheet = ezodf.Sheet('REFS', size=(NROWS, NCOLS))
ods.sheets += sheet

for row in range(NROWS):
    for col in range(NCOLS):
        content = chr(ord('A') + col) + str(row+1)
        sheet[row, col].set_value(content)

ods.save()
