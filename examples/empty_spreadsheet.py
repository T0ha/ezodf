#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: empty spreadsheet
# Created: 26.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import ezodf

ods = ezodf.newdoc('ods', "empty_spreadsheet.ods")
for sheet in [ezodf.Sheet(name='TEST1', size=(20, 10)),
              ezodf.Sheet(name='TEST2', size=(20, 10)),
              ezodf.Sheet(name='TEST3', size=(20, 10)),]:
    ods.body.append(sheet)
ods.save()