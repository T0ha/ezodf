#!/usr/bin/env python
#coding:utf-8
# Purpose: swap row/columns of a table
# Created: 04.10.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

import ezodf

ROWS, COLS = 20, 10

# create a new spreadsheet document
doc = ezodf.newdoc(doctype="ods", filename="my_spreadsheet.ods")
# create a new table
table = ezodf.Table(name="Table", size=(ROWS, COLS))
# add table to document
doc.sheets += table

# set table values
for row in range(ROWS):
    for col in range(COLS):
        content = "%s%s" % (chr(65+col), row+1)
        cell = table[row, col]
        cell.set_value(content)

# create the symmetric table
symtable = ezodf.Table(name="Symmetry", size=(COLS, ROWS))
doc.sheets += symtable

# set symmetric values
for row in range(ROWS):
    for col in range(COLS):
        source_cell = table[row, col]
        target_cell = symtable[col, row]
        target_cell.set_value(source_cell.value)

# alternative way
symtable= ezodf.Table(name="Symmetry(2)", size=(COLS, ROWS))
doc.sheets += symtable

# process table by itercells()
for pos, cell in table.itercells():
    symtable[ pos[1], pos[0] ].set_value(cell.value)
    
print("Spreadsheet contains %d sheets.\n" % len(doc.sheets))
for sheet in doc.sheets:
    print("Sheet name: '%s'" % sheet.name)
    print("Size of Sheet : (%d, %d)" % (sheet.nrows(), sheet.ncols()) )
    print("-"*40)
    
doc.save()
