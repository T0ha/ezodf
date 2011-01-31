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
from .propertymixins import NumberColumnsRepeatedMixin, VisibilityMixin
from .propertymixins import StylenNameMixin, DefaultCellStyleNameMixin

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
class Table(GenericWrapper, StylenNameMixin):
    TAG = CN('table:table')

    def __init__(self, name='NEWTABLE', size=(10, 10), xmlnode=None):
        super(Table, self).__init__(xmlnode=xmlnode)
        self._cell_cache = {}
        if xmlnode is None:
            self.name = name
            self._setup(size)
        else:
            self._expand_repeated_table_content()

    def _setup(self, size):
        def validate_parameter(nrows, ncols):
            if nrows < 1:
                raise ValueError('nrows has to be >= 1.')
            if ncols < 1:
                raise ValueError('ncols has to be >= 1.')

        nrows, ncols = size
        validate_parameter(nrows, ncols)
        for row in range(nrows):
            self.append(TableRow(ncols=ncols))
        wrapcache.add(self)
        self._reset_cell_cache()

    def _reset_cell_cache(self):
        self._cell_cache.clear()

    def _expand_repeated_table_content(self):

        def expand_element(count, element):
            xmlnode = element.xmlnode
            while count > 1:
                clone = copy.deepcopy(xmlnode)
                xmlnode.addnext(clone)
                count -= 1

        def expand_cells(row):
            # convert to list, because we modify content of row
            for cell in list(iter(row)):
                count = cell.columns_repeated
                if count > 1:
                    cell.clear_columns_repeated_attribute()
                    expand_element(count, cell)

        def expand_row(row):
            count = row.rows_repeated
            row.clear_rows_repeated_attribute()
            expand_element(count, row)

        for row in self.findall(TableRow.TAG):
            expand_cells(row)
            if row.rows_repeated > 1:
                expand_row(row)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.get_child(key)
        elif isinstance(key, tuple):
            # key => (row, column)
            return self.get_cell_by_index(key)
        elif isinstance(key, str):
            # key => 'A1'
            return self.get_cell_by_address(key)
        else:
            raise TypeError(str(type(key)))

    def __setitem__(self, key, value):
        if isinstance(key, int):
            return self.set_child(key, value)
        elif isinstance(key, tuple):
            # key => (row, column)
            return self.set_cell_by_index(key, value)
        elif isinstance(key, str):
            # key => 'A1'
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
        # assume that all repeated rows are expanded
        return len(list(self.findall(TableRow.TAG)))

    def ncols(self):
        """ Count of table columns. """
        # assume that all repeated columns are expanded
        first_row = self.find(TableRow.TAG)
        return 0 if first_row is None else len(first_row.xmlnode)

    def clear(self, size=(10, 10)):
        super(Table, self).clear()
        self._setup(size)

    def get_cell_by_index(self, pos):
        """ Get cell at position 'pos', where 'pos' is a tuple (row, column). """
        try:
            return self._cell_cache[pos]
        except KeyError:
            row, column = pos
            if row < 0 or column < 0 :
                raise IndexError('negative indices not allowed.')

            table_row = self._get_row_at_index(row)
            return self._wrap(pos, table_row[column])

    def _wrap(self, pos, xmlnode):
        cell = wrap(xmlnode)
        self._cell_cache[pos] = cell
        return cell

    def get_cell_by_address(self, address):
        """ Get cell at position 'address' ('address' like 'A1'). """
        pos = address_to_index(address)
        return self.get_cell_by_index(pos)

    def set_cell_by_index(self, pos, cell):
        """ Set cell at position 'pos', where 'pos' is a tuple (row, column). """
        if not hasattr(cell, 'kind') or cell.kind != 'Cell':
            raise TypeError("invalid type of 'cell'.")
        row, column = pos
        if row < 0 or column < 0 :
            raise IndexError('negative indices not allowed.')

        table_row = self._get_row_at_index(row)
        table_row[column] = cell.xmlnode
        self._cell_cache[pos] = cell

    def set_cell_by_address(self, address, cell):
        """ Set cell at position 'address' ('address' like 'A1'). """
        pos = address_to_index(address)
        return self.set_cell_by_index(pos, cell)

    def _get_index_of_first_row(self):
        first_row = self.xmlnode.find(CN('table:table-row'))
        if first_row is not None:
            return self.xmlnode.index(first_row)
        else:
            raise IndexError('no rows in table')

    def _get_row_at_index(self, index):
        first_row_index = self._get_index_of_first_row()
        return self.xmlnode[first_row_index+index]

    def row(self, index):
        if isinstance(index, str):
            index, column = address_to_index(index)
        if index < 0:
            raise IndexError('row index out of range: %s' % index)
        return ( self._wrap((index, col), xmlnode) for col, xmlnode in \
                 enumerate(self._get_row_at_index(index)) )

    def rows(self):
        for xmlrow in self._xmlrows():
            yield (wrap(xmlcell) for xmlcell in xmlrow)

    def _xmlrows(self):
        return self.xmlnode.findall(CN('table:table-row'))

    def column(self, index):
        if isinstance(index, str):
            row, index = address_to_index(index)
        if index < 0 or index >= self.ncols():
            raise IndexError('row index out of range: %s' % index)
        return ( self._wrap((xrow,index), row[index]) for xrow, row in \
                 enumerate(self.xmlnode.findall(CN('table:table-row'))) )

    def append_rows(self, count=1):
        Table._validate_count_parameter(count)
        ncols = self.ncols()
        last_xmlrow = self._xmlrows()[-1]
        for index in range(count):
            last_xmlrow.addnext(Table._new_xmlrow(ncols))

    @staticmethod
    def _new_xmlrow(count):
        xmlrow = etree.Element(CN('table:table-row'))
        for _ in range(count):
            xmlrow.append(etree.Element(CN('table:table-cell')))
        return xmlrow

    def insert_rows(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        Table._validate_insert_parameters(index, count, self.nrows())
        index += self._get_index_of_first_row()
        ncols = self.ncols()
        for _ in range(count):
            self.xmlnode.insert(index, Table._new_xmlrow(ncols))
        self._reset_cell_cache()

    @staticmethod
    def _validate_insert_parameters(index, insert_count, element_count):
        Table._validate_index_parameter(index, element_count)
        Table._validate_count_parameter(insert_count)

    @staticmethod
    def _validate_count_parameter(count):
        if count < 1:
            raise ValueError("count: %d" % count)

    @staticmethod
    def _validate_index_parameter(index, element_count):
        if index < 0 or index >= element_count:
            raise IndexError("index: %d" % index)

    def delete_rows(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        Table._validate_delete_parameters(index, count, self.nrows())
        index += self._get_index_of_first_row()
        for _ in range(count):
            del self.xmlnode[index]
        self._reset_cell_cache()

    @staticmethod
    def _validate_delete_parameters(index, delete_count, element_count):
        Table._validate_index_parameter(index, element_count)
        Table._validate_count_parameter(delete_count)
        if (index+delete_count-1) >= element_count:
            raise IndexError("index+count: %d" % (index+delete_count))

    def append_columns(self, count=1):
        Table._validate_count_parameter(count)
        for xmlrow in self._xmlrows():
            for _ in range(count):
                xmlrow.append(etree.Element(CN('table:table-cell')))

    def insert_columns(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        Table._validate_insert_parameters(index, count, self.ncols())
        for xmlrow in self._xmlrows():
            for _ in range(count):
                xmlrow.insert(index, etree.Element(CN('table:table-cell')))
        self._reset_cell_cache()

    def delete_columns(self, index, count=1):
        # CAUTION: this will break refernces in formulas!
        Table._validate_delete_parameters(index, count, self.ncols())
        for xmlrow in self._xmlrows():
            for _ in range(count):
                del xmlrow[index]
        self._reset_cell_cache()

@register_class
class TableRow(GenericWrapper, StylenNameMixin, VisibilityMixin,
               DefaultCellStyleNameMixin):
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
class TableColumn(GenericWrapper, StylenNameMixin, VisibilityMixin,
                  DefaultCellStyleNameMixin, NumberColumnsRepeatedMixin):
    TAG = CN('table:table-column')
