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
from .propertymixins import TableNumberColumnsRepeatedMixin, TableVisibilityMixin
from .propertymixins import TableStylenNameMixin, TableDefaultCellStyleNameMixin
from .tablerowcontainer import TableRowContainer

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
        self.cells = TableRowContainer(self.xmlnode)
        if xmlnode is None:
            self.name = name
            self.cells.reset(size)
        else:
            self.cells.buildup()
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

    def __setitem__(self, key, value):
        if isinstance(key, int):
            return self.set_child(key, value)
        elif isinstance(key, tuple): # key => (row, column)
            return self.set_cell_by_index(key, value)
        elif isinstance(key, str): # key => 'A1'
            return self.set_cell_by_address(key, value)
        else:
            raise TypeError(str(type(key)))

    @property
    def name(self):
        return self.get_attr(CN('table:name'))
    @name.setter
    def name(self, value):
        return self.set_attr(CN('table:name'), value)

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
        return self.cells.nrows()

    def ncols(self):
        """ Count of table columns. """
        return self.cells.ncols()

    def clear(self, size=(10, 10)):
        super(Table, self).clear()
        self.cells.reset(size)

    def get_cell_by_index(self, pos):
        """ Get cell at position 'pos', where 'pos' is a tuple (row, column). """
        return wrap(self.cells.get_cell(pos))

    def get_cell_by_address(self, address):
        """ Get cell at position 'address' ('address' like 'A1'). """
        pos = address_to_index(address)
        return self.get_cell_by_index(pos)

    def set_cell_by_index(self, pos, cell):
        """ Set cell at position 'pos', where 'pos' is a tuple (row, column). """
        if not hasattr(cell, 'kind') or cell.kind != 'Cell':
            raise TypeError("invalid type of 'cell'.")
        self.cells.set_cell(pos, cell.xmlnode)

    def set_cell_by_address(self, address, cell):
        """ Set cell at position 'address' ('address' like 'A1'). """
        pos = address_to_index(address)
        return self.set_cell_by_index(pos, cell)

    def row(self, index):
        if isinstance(index, str):
            index, column = address_to_index(index)
        return (wrap(e) for e in self.cells.row(index))

    def rows(self):
        for xmlrow in self.cells.rows():
            yield (wrap(xmlcell) for xmlcell in xmlrow)

    def column(self, index):
        if isinstance(index, str):
            row, index = address_to_index(index)
        return (wrap(e) for e in self.cells.column(index))

    def append_rows(self, count=1):
        self.cells.append_rows(count)

    def insert_rows(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        self.cells.insert_rows(index, count)

    def delete_rows(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        self.cells.delete_rows(index, count)

    def append_columns(self, count=1):
        self.cells.append_columns(count)

    def insert_columns(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        self.cells.insert_columns(index, count)

    def delete_columns(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        self.cells.delete_columns(index, count)

@register_class
class TableRow(GenericWrapper, TableStylenNameMixin, TableVisibilityMixin,
               TableDefaultCellStyleNameMixin):
    TAG = CN('table:table-row')

    def __init__(self, ncols=10, xmlnode=None):
        super(TableRow, self).__init__(xmlnode=xmlnode)
        if xmlnode is None:
            self._setup(ncols)

    def _setup(self, ncols):
        for col in range(ncols):
            self.xmlnode.append(etree.Element(CN('table:table-cell')))

    @property
    def rows_repeated(self):
        value = self.get_attr(CN('table:number-rows-repeated'))
        value = int(value) if value is not None else 1
        return max(1, value)

    def clear_rows_repeated_attribute(self):
        del self.xmlnode.attrib[CN('table:number-rows-repeated')]

@register_class
class TableColumn(GenericWrapper, TableStylenNameMixin, TableVisibilityMixin,
                  TableDefaultCellStyleNameMixin, TableNumberColumnsRepeatedMixin):
    TAG = CN('table:table-column')
