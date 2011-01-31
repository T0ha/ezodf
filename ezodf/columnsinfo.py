#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: ColumnsInfo class
# Created: 31.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import copy

from .xmlns import CN, etree, wrap

table_prelude = frozenset([
    CN("table:table-source"),
    CN("office:dde-source"),
    CN("table:scenario"),
    CN("office:forms"),
    CN("table:shapes")])

def get_insert_pos(xmlnode):
    maxindex = -1
    for index, child in enumerate(xmlnode.iterchildren()):
        if child.tag in table_prelude:
            maxindex = index
    return maxindex + 1

class ColumnsInfo:
    def __init__(self, xmlnode, ncols=10):
        self.xmlnode = xmlnode
        self._setup(ncols)

    def _setup(self, ncols):
        if self.xmlnode.find(CN('table:table-column')) is None:
            self._new_columns(ncols)
        else:
            self._expand_columns()

    def _new_columns(self, ncols):
        insert_pos = get_insert_pos(self.xmlnode)
        for _ in range(ncols):
            self.xmlnode.insert(insert_pos, etree.Element(CN('table:table-column')))

    def _expand_columns(self):
        def expand(xmlnode, count):
            while count > 1:
                clone = copy.deepcopy(xmlnode)
                xmlnode.addnext(clone)
                count -= 1

        def get_repeat_count(xmlnode):
            repeated = xmlnode.get(CN('table:number-columns-repeated'))
            return int(repeated) if repeated else 1

        for xmlcolumn in self.xmlnode.findall(CN('table:table-column')):
            expand(xmlcolumn, get_repeat_count(xmlcolumn))

    def ncols(self):
        return len(self.xmlnode.findall(CN('table:table-column')))

