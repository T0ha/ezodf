#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: table objects
# Created: 03.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import re
import copy

from .xmlns import register_class, CN, wrap, etree
from . import wrapcache
from .base import GenericWrapper
from .protection import random_protection_key
from .propertymixins import TableVisibilityMixin
from .propertymixins import TableStylenNameMixin, TableDefaultCellStyleNameMixin
from .tablerowcontainer import TableRowContainer
from .tablecolumncontainer import TableColumnContainer

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

    res = CELL_ADDRESS.match(address)
    if res:
        column_name, row_name = res.groups()
        return (int(row_name)-1, column_name_to_index(column_name))
    else:
        raise ValueError('Invalid cell address: %s' % address)

@register_class
class Table(GenericWrapper, TableStylenNameMixin):
    TAG = CN('table:table')

    def __init__(self, name='NEWTABLE', size=(10, 10), xmlnode=None):
        super(Table, self).__init__(xmlnode=xmlnode)
        self._rows = TableRowContainer(self.xmlnode)
        self._columns = TableColumnContainer(self.xmlnode)
        if xmlnode is None:
            self.name = name
            self._rows.reset(size)
            self._columns.reset(size[1])
        else:
            self._rows.buildup()
            self._columns.buildup()
        wrapcache.add(self)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.get_child(key)
        elif isinstance(key, tuple): # key => (row, column)
            return self.get_cell_by_index(key)
        elif isinstance(key, str): # key => 'A1'
            return self.get_cell_by_address(key)
        else:
            raise TypeError(str(type(key)))

    def __setitem__(self, key, cell):
        if isinstance(key, int):
            return self.set_child(key, cell)
        elif isinstance(key, tuple): # key => (row, column)
            return self.set_cell_by_index(key, cell)
        elif isinstance(key, str): # key => 'A1'
            return self.set_cell_by_address(key, cell)
        else:
            raise TypeError(str(type(key)))

    @property
    def name(self):
        return self.get_attr(CN('table:name'))
    @name.setter
    def name(self, value):
        return self.set_attr(CN('table:name'), self._normalize_sheet_name(value))

    @staticmethod
    def _normalize_sheet_name(name):
        for subst in "\t\r'\"":
            name = name.replace(subst, ' ')
        return name.strip()

    @property
    def protected(self):
        return self.get_bool_attr(CN('table:protected'))
    @protected.setter
    def protected(self, value):
        self.set_bool_attr(CN('table:protected'), value)
        if self.protected:
            self.set_attr(CN('table:protection-key'), random_protection_key())

    @property
    def print(self):
        return self.get_bool_attr(CN('table:print'))
    @print.setter
    def print(self, value):
        self.set_bool_attr(CN('table:print'), value)

    def nrows(self):
        """ Count of table rows. """
        return self._rows.nrows()

    def ncols(self):
        """ Count of table columns. """
        return self._rows.ncols()

    def reset(self, size=(10, 10)):
        super(Table, self).clear()
        self._rows.reset(size)
        self._columns.reset(size[1])

    def clear(self):
        raise NotImplementedError("for tables use the reset() method.")

    def copy(self, newname=None):
        newtable = Table(xmlnode=copy.deepcopy(self.xmlnode))
        if newname is None:
            newname = 'CopyOf' + self.name
        newtable.name = newname
        return newtable

    def get_cell_by_index(self, pos):
        """ Get cell at position 'pos', where 'pos' is a tuple (row, column). """
        return wrap(self._rows.get_cell(pos))

    def get_cell_by_address(self, address):
        """ Get cell at position 'address' ('address' like 'A1'). """
        pos = address_to_index(address)
        return self.get_cell_by_index(pos)

    def set_cell_by_index(self, pos, cell):
        """ Set cell at position 'pos', where 'pos' is a tuple (row, column). """
        if not hasattr(cell, 'kind') or cell.kind != 'Cell':
            raise TypeError("invalid type of 'cell'.")
        self._rows.set_cell(pos, cell.xmlnode)

    def set_cell_by_address(self, address, cell):
        """ Set cell at position 'address' ('address' like 'A1'). """
        pos = address_to_index(address)
        return self.set_cell_by_index(pos, cell)

    def row(self, index):
        if isinstance(index, str):
            index, column = address_to_index(index)
        return [wrap(e) for e in self._rows.row(index)]

    def rows(self):
        for index in range(self.ncols()):
            yield self.row(index)

    def column(self, index):
        if isinstance(index, str):
            row, index = address_to_index(index)
        return [wrap(e) for e in self._rows.column(index)]

    def columns(self):
        for index in range(self.ncols()):
            yield self.column(index)

    def row_info(self, index):
        if isinstance(index, str):
            index, column = address_to_index(index)
        return wrap(self._rows.get_table_row(index))

    def column_info(self, index):
        if isinstance(index, str):
            row, index = address_to_index(index)
        return wrap(self._columns.get_table_column(index))

    def append_rows(self, count=1):
        self._rows.append_rows(count)

    def insert_rows(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        self._rows.insert_rows(index, count)

    def delete_rows(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        self._rows.delete_rows(index, count)

    def append_columns(self, count=1):
        self._rows.append_columns(count)
        self._columns.append(count)

    def insert_columns(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        self._rows.insert_columns(index, count)
        self._columns.insert(index, count)

    def delete_columns(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        self._rows.delete_columns(index, count)
        self._columns.delete(index, count)

@register_class
class TableColumn(GenericWrapper, TableStylenNameMixin, TableVisibilityMixin,
                  TableDefaultCellStyleNameMixin):
    TAG = CN('table:table-column')

@register_class
class TableRow(TableColumn):
    TAG = CN('table:table-row')

    def __init__(self, ncols=10, xmlnode=None):
        super(TableRow, self).__init__(xmlnode=xmlnode)
        if xmlnode is None:
            self._setup(ncols)

    def _setup(self, ncols):
        for col in range(ncols):
            self.xmlnode.append(etree.Element(CN('table:table-cell')))

