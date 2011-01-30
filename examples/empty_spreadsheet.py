#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: empty spreadsheet
# Created: 26.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import ezodf

ods = ezodf.newdoc('ods', "empty_spreadsheet.ods")
for sheetname in ['SHEET1', 'SHEET2', 'SHEET3']:
    ods.sheets += ezodf.Sheet(name=sheetname, size=(20, 10))

ods.save()