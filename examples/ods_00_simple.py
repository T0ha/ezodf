#!/usr/bin/env python
#coding:utf-8
# Purpose: simple spreadsheet
# Created: 26.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

import ezodf

ods = ezodf.newdoc('ods', "simple_spreadsheet.ods")

sheet = ezodf.Sheet('NUMBERS', size=(20, 10))
ods.sheets += sheet
for index in range(sheet.ncols()):
    sheet[5, index].set_value(index)
    sheet[index, 5].set_value(index)
    sheet[index, index].set_value(index, value_type='currency', currency='EUR')

sheet = ezodf.Sheet('TEXT', size=(20, 10))
ods.sheets += sheet
for column in range(sheet.ncols()):
    for row, cell in enumerate(sheet.column(column)):
        cell.set_value("Cell (%d, %d)" % (row, column))
ods.save()
