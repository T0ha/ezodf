#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: empty spreadsheet
# Created: 26.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import ezodf

ods = ezodf.newdoc('ods', "empty_spreadsheet.ods")
for sheetname in ['TEST1', 'TEST2', 'TEST3']:
    ods.sheets += ezodf.Sheet(name=sheetname, size=(20, 10))

sheet = ods.sheets['TEST2']
for index in range(sheet.ncols()):
    sheet[5, index] = ezodf.Cell(index)
    sheet[index, 5] = ezodf.Cell(index)
    sheet[index, index] = ezodf.Cell(index)
ods.save()