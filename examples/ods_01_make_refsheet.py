#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: example make_refshett.py
# Created: 05.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

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