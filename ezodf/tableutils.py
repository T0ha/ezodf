#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: table utils
# Created: 13.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import re

def iter_cell_range(pos, size):
    start_row, start_column = pos
    if (start_row < 0) or (start_column < 0):
        raise ValueError("invalid start pos: %s" % str(pos))
    nrows, ncolumns = size
    if (nrows < 1) or (ncolumns < 1):
        raise ValueError("invalid size: %s" % str(size))

    for row in range(start_row, start_row + nrows):
        for column in range(start_column, start_column + ncolumns):
            yield (row, column)

CELL_ADDRESS = re.compile('^([A-Z]+)(\d+)$')

def address_to_index(address):
    def column_name_to_index(colname):
        index = 0
        power = 1
        base = ord('A') - 1
        for char in reversed(colname):
            index += (ord(char) - base) * power
            power *= 26
        return index - 1

    res = CELL_ADDRESS.match(address.upper())
    if res:
        column_name, row_name = res.groups()
        return (int(row_name)-1, column_name_to_index(column_name))
    else:
        raise ValueError('Invalid cell address: %s' % address)

def get_cell_index(reference):
    if isinstance(reference, tuple): # key => (row, column)
        return reference
    elif isinstance(reference, str): # key => 'A1'
        return address_to_index(reference)
    else:
        raise TypeError(str(type(key)))
