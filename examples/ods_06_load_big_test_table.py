#!/usr/bin/env python
#coding:utf-8
# Purpose: swap row/columns of a table
# Created: 28.05.2012
# Copyright (C) 2012, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

import ezodf

# open spreadsheet document
doc = ezodf.opendoc("big-test-table.ods")
    
print("Spreadsheet contains %d sheets.\n" % len(doc.sheets))
for sheet in doc.sheets:
    print("Sheet name: '%s'" % sheet.name)
    print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
    print("-"*40)
    
doc.save()
