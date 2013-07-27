#!/usr/bin/env python
#coding:utf-8
# Purpose: example insertcolumns.py
# Created: 05.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

import ezodf

ods = ezodf.opendoc('refsheet.ods')

sheet = ods.sheets[0]
sheet.insert_columns(5, 3)
sheet.insert_rows(5, 3)

for row in range(sheet.nrows()):
    for col in range(5, 8):
        content = '+COL' + str(col)
        sheet[row, col].set_value(content)

for col in range(sheet.ncols()):
    for row in range(5, 8):
        content = '+ROW' + str(row)
        sheet[row, col].set_value(content)

ods.save()
