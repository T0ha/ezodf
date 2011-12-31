#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: table nomalizer
# Created: 14.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import copy

from .xmlns import CN
from .tableutils import new_empty_cell, get_table_rows, is_table
from .tableutils import get_min_max_cell_count, count_cells_in_row
from .tableutils import RepetitionAttribute

class TableNormalizer(object):
    def __init__(self, xmlnode):
        if not is_table(xmlnode):
            raise ValueError('invalid xmlnode')
        self.xmlnode = xmlnode

    def expand_repeated_table_content(self):
        def expand_element(xmlnode, count):
            while count > 1:
                clone = copy.deepcopy(xmlnode)
                xmlnode.addnext(clone)
                count -= 1

        def expand_cell(xmlcell, count):
            if count > 1:
                del RepetitionAttribute(xmlcell).cols
                expand_element(xmlcell, count)

        def expand_cells(xmlrow):
            for xmlcell in xmlrow:
                expand_cell(xmlcell, RepetitionAttribute(xmlcell).cols)

        def expand_row(xmlrow):
            count = RepetitionAttribute(xmlrow).rows
            del RepetitionAttribute(xmlrow).rows
            expand_element(xmlrow, count)

        for xmlrow in get_table_rows(self.xmlnode):
            expand_cells(xmlrow)
            if RepetitionAttribute(xmlrow).rows > 1:
                expand_row(xmlrow)

    def align_table_columns(self):
        def append_cells(xmlrow, count):
            for _ in range(count):
                xmlrow.append(new_empty_cell())

        def _align_table_columns(required_cells_per_row):
            for xmlrow in get_table_rows(self.xmlnode):
                count = count_cells_in_row(xmlrow)
                if count < required_cells_per_row:
                    append_cells(xmlrow, required_cells_per_row - count)

        cmin, cmax = get_min_max_cell_count(self.xmlnode)
        if cmin != cmax:
            _align_table_columns(cmax)

def normalize_table(xmlnode):
    normalizer = TableNormalizer(xmlnode)
    normalizer.expand_repeated_table_content()
    normalizer.align_table_columns()
