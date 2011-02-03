#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: table-row container
# Created: 02.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import copy

from .xmlns import CN, etree
from .nodestructuretags import TABLE_ROWS

def get_columns_repeated(xmlnode):
    count = xmlnode.get(CN('table:number-columns-repeated'))
    return 1 if count is None else int(count)

def del_columns_repeated(xmlnode):
    del xmlnode.attrib[CN('table:number-columns-repeated')]

def get_rows_repeated(xmlnode):
    count = xmlnode.get(CN('table:number-rows-repeated'))
    return 1 if count is None else int(count)

def del_rows_repeated(xmlnode):
    del xmlnode.attrib[CN('table:number-rows-repeated')]

def new_empty_cell():
    return etree.Element(CN('table:table-cell'))

class TableRowContainer:
    def __init__(self, xmlnode):
        if xmlnode is None or xmlnode.tag != CN('table:table'):
            raise ValueError('invalid xmlnode')
        self.xmlnode = xmlnode
        self.buildup()

    def buildup(self):
        self._expand_repeated_table_content()
        self.update()

    def update(self):
        self._rows = self.xmlnode.findall('.//'+CN('table:table-row'))

    def reset(self, size):
        def validate_parameter(nrows, ncols):
            if nrows < 1:
                raise ValueError('nrows has to be >= 1.')
            if ncols < 1:
                raise ValueError('ncols has to be >= 1.')

        self._remove_existing_rows()
        nrows, ncols = size
        validate_parameter(nrows, ncols)
        row = self._buildrow(ncols)
        for _ in range(nrows):
            self.xmlnode.append(copy.deepcopy(row))
        self.update()

    @staticmethod
    def _buildrow(ncols):
        row = etree.Element(CN('table:table-row'))
        for _ in range(ncols):
            row.append(new_empty_cell())
        return row

    def _remove_existing_rows(self):
        for child in self.xmlnode.getchildren():
            if child.tag in TABLE_ROWS:
                self.xmlnode.remove(child)

    def _expand_repeated_table_content(self):
        def expand_element(count, xmlnode):
            while count > 1:
                clone = copy.deepcopy(xmlnode)
                xmlnode.addnext(clone)
                count -= 1

        def expand_cells(xmlrow):
            for cell in xmlrow.getchildren():
                count = get_columns_repeated(cell)
                if count > 1:
                    del_columns_repeated(cell)
                    expand_element(count, cell)

        def expand_row(xmlrow):
            count = get_rows_repeated(xmlrow)
            del_rows_repeated(xmlrow)
            expand_element(count, xmlrow)

        for xmlrow in self.xmlnode.findall('.//'+CN('table:table-row')):
            expand_cells(xmlrow)
            if get_rows_repeated(xmlrow) > 1:
                expand_row(xmlrow)

    def nrows(self):
        return len(self._rows)

    def ncols(self):
        return len(self._rows[0]) if self.nrows() > 0 else 0

    def get_cell(self, pos):
        row, col = self._get_row_col(pos)
        return self._rows[row][col]

    def set_cell(self, pos, element):
        row, col = self._get_row_col(pos)
        self._rows[row][col] = element

    def _get_row_col(self, pos):
        row, col = pos
        if row < 0:
            row += self.nrows()
        if col < 0:
            col += self.ncols()
        return (row, col)

    def get_table_row(self, index):
        return self._rows[index]

    def row(self, index):
        return self._rows[index]

    def column(self, index):
        return [row[index] for row in self._rows]

    def rows(self):
        return self._rows

    def is_consistent(self):
        # just for testing
        xmlrows = self.xmlnode.findall('.//'+CN('table:table-row'))
        if len(xmlrows) != len(self._rows):
            return False
        for row1, row2 in zip(self._rows, xmlrows):
            if row1 != row2:
                return False
        return True

    def append_rows(self, count=1):
        if count < 1:
            raise ValueError('count < 1')
        for _ in range(count):
            newrow = self._buildrow(self.ncols())
            last_row = self._rows[-1]
            last_row.addnext(newrow)
            self._rows.append(newrow)

    def insert_rows(self, index, count=1):
        if count < 1:
            raise ValueError('count < 1')
        for _ in range(count):
            newrow = self._buildrow(self.ncols())
            insert_row = self._rows[index]
            insert_row.addprevious(newrow)
            self._rows.insert(index, newrow)

    def delete_rows(self, index, count=1):
        if count < 1:
            raise ValueError('count < 1')
        if index < 0:
            index += self.nrows()

        for _ in range(count):
            delete_row = self._rows.pop(index)
            delete_row.getparent().remove(delete_row)

    def append_columns(self, count=1):
        if count < 1:
            raise ValueError('count < 1')
        for row in self._rows:
            for _ in range(count):
                row.append(new_empty_cell())

    def insert_columns(self, index, count=1):
        if count < 1:
            raise ValueError('count < 1')
        if index < 0:
            index += self.ncols()

        for row in self._rows:
            for _ in range(count):
                row.insert(index, new_empty_cell())

    def delete_columns(self, index, count=1):
        if count < 1:
            raise ValueError('count < 1')
        if index < 0:
            index += self.ncols()
        for row in self._rows:
            for _ in range(count):
                del row[index]
