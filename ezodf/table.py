#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: table objects
# Created: 03.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3


import copy

from .xmlns import register_class, CN, wrap, etree
from . import wrapcache
from .base import GenericWrapper
from .protection import random_protection_key
from .propertymixins import TableVisibilityMixin
from .propertymixins import TableStylenNameMixin, TableDefaultCellStyleNameMixin
from .tableutils import address_to_index, get_cell_index
from .tablerowcontroller import TableRowController
from .tablecolumncontroller import TableColumnController
from .cellspancontroller import CellSpanController

@register_class
class Table(GenericWrapper, TableStylenNameMixin):
    TAG = CN('table:table')

    def __init__(self, name='NEWTABLE', size=(10, 10), xmlnode=None):
        super(Table, self).__init__(xmlnode=xmlnode)
        self._rows = TableRowController(self.xmlnode)
        self._columns = TableColumnController(self.xmlnode)
        self._cell_span_controller = CellSpanController(self._rows)

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
        else:
            return self._get_cell(get_cell_index(key))

    def __setitem__(self, key, cell):
        if isinstance(key, int):
            return self.set_child(key, cell)
        else:
            self._set_cell(get_cell_index(key), cell)

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

    def _get_cell(self, pos):
        """ Get cell at position 'pos', where 'pos' is a tuple (row, column). """
        return wrap(self._rows.get_cell(pos))

    def _set_cell(self, pos, cell):
        """ Set cell at position 'pos', where 'pos' is a tuple (row, column). """
        if not hasattr(cell, 'kind') or cell.kind != 'Cell':
            raise TypeError("invalid type of 'cell'.")
        self._rows.set_cell(pos, cell.xmlnode)

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

    def set_cell_span(self, pos, size):
        self._cell_span_controller.set_span(get_cell_index(pos), size)

    def remove_cell_span(self, pos):
        self._cell_span_controller.remove_span(get_cell_index(pos))

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

