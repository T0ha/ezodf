#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: sheets object
# Created: 29.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import CN
from . import wrapcache

def _is_table(table):
    if hasattr(table, 'kind') and table.kind == 'Table':
        return True
    else:
        return False

class Sheets:
    def __init__(self, xmlbody):
        self.xmlnode = xmlbody

    def __len__(self):
        return len(self._xmlsheets())

    def __iter__(self):
        return (wrapcache.wrap(sheet) for sheet in self._xmlsheets())

    def _xmlsheets(self):
        return self.xmlnode.findall(CN('table:table'))

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.sheet_by_index(key)
        elif isinstance(key, str):
            return self.sheet_by_name(key)
        else:
            raise TypeError('key has invalid type.')

    def __setitem__(self, key, sheet):
        if not _is_table(sheet):
            raise TypeError('sheet has to be a Table/Sheet.')
        if isinstance(key, int):
            oldsheet = self.sheet_by_index(key)
        elif isinstance(key, str):
            oldsheet = self.sheet_by_name(key)
        else:
            raise TypeError('key has invalid type.')
        self.xmlnode.replace(oldsheet.xmlnode, sheet.xmlnode)

    def __delitem__(self, key):
        if isinstance(key, int):
            oldsheet = self.sheet_by_index(key)
        elif isinstance(key, str):
            oldsheet = self.sheet_by_name(key)
        else:
            raise TypeError('key has invalid type.')
        self.xmlnode.remove(oldsheet.xmlnode)

    def __iadd__(self, other):
        self.append(other)
        return self

    def sheet_by_name(self, name):
        for sheet in self._xmlsheets():
            if name == sheet.get(CN('table:name')):
                return wrapcache.wrap(sheet)
        raise KeyError("sheet '%s' not found." % name)

    def sheet_by_index(self, index):
        sheets = list(self._xmlsheets())
        return wrapcache.wrap(sheets[index])

    def append(self, sheet):
        if _is_table(sheet):
            self.xmlnode.append(sheet.xmlnode)
            return sheet
        else:
            raise TypeError('Unable to append: %s' % str(sheet))

    def names(self):
        return (sheet.get(CN('table:name')) for sheet in self._xmlsheets())

    def index(self, sheet):
        return self.xmlnode.index(sheet.xmlnode)

    def insert(self, index, sheet):
        self.xmlnode.insert(int(index), sheet.xmlnode)
        return sheet
