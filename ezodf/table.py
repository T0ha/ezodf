#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: table objects
# Created: 03.01.2011
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import re
import copy
from datetime import timedelta, date

from .xmlns import register_class, CN, wrap
from .base import GenericWrapper
from .protection import random_protection_key
from .text import Paragraph, Span

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

class _StylenNameMixin:
    @property
    def style_name(self):
        return self.get_attr(CN('table:style-name'))
    @style_name.setter
    def style_name(self, name):
        self.set_attr(CN('table:style-name'), name)

class _DefaultCellStyleNameMixin:
    @property
    def default_cell_style_name(self):
        return self.get_attr(CN('table:default-cell-style-name'))
    @default_cell_style_name.setter
    def default_cell_style_name(self, value):
        self.set_attr(CN('table:default-cell-style-name'), value)

class _VisibilityMixin:
    VALID_VISIBILITY_STATES = frozenset( ('visible', 'collapse', 'filter') )
    @property
    def visibility(self):
        value = self.get_attr(CN('table:visibility'))
        if value is None:
            value = 'visible'
        return value
    @visibility.setter
    def visibility(self, value):
        if value not in self.VALID_VISIBILITY_STATES:
            raise ValueError("allowed values are: 'visible', 'collapse', 'filter'")
        self.set_attr(CN('table:visibility'), value)

class _NumberColumnsRepeatedMixin:
    @property
    def columns_repeated(self):
        value = self.get_attr(CN('table:number-columns-repeated'))
        value = int(value) if value is not None else 1
        return max(1, value)
    def clear_columns_repeated(self):
        del self.xmlnode.attrib[CN('table:number-columns-repeated')]

@register_class
class Table(GenericWrapper, _StylenNameMixin):
    TAG = CN('table:table')

    def __init__(self, name='NEWTABLE', size=(10, 10), xmlnode=None):
        super(Table, self).__init__(xmlnode=xmlnode)
        self._cell_cache = {}
        if xmlnode is None:
            self.name = name
            self._setup(size[0], size[1])
        else:
            self._expand_repeated_table_content()

    def _setup(self, nrows, ncols):
        for row in range(nrows):
            self.append(TableRow(ncols=ncols))
        self._reset_cache()

    def _reset_cache(self):
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
                    cell.clear_columns_repeated()
                    expand_element(count, cell)

        def expand_row(row):
            count = row.rows_repeated
            row.clear_rows_repeated()
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

    def clear(self):
        super(Table, self).clear()
        self._reset_cache()

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
        try:
            # if possible return same wrapper to preserve caches
            cell = self._cell_cache[pos]
            if cell.xmlnode is xmlnode:
                return cell
        except KeyError:
            pass
        cell = wrap(xmlnode)
        self._cell_cache[pos] = cell
        return cell

    def get_cell_by_address(self, address):
        """ Get cell at position 'address' ('address' like 'A1'). """
        pos = address_to_index(address)
        return self.get_cell_by_index(pos)

    def set_cell_by_index(self, pos, cell):
        """ Set cell at position 'pos', where 'pos' is a tuple (row, column). """
        if not isinstance(cell, Cell):
            raise TypeError("invalid type of 'cell'.")
        row, column = pos
        if row < 0 or column < 0 :
            raise IndexError('negative indices not allowed.')

        # write-thru cache
        table_row = self._get_row_at_index(row)
        table_row[column] = cell.xmlnode
        self._cell_cache[pos] = cell

    def set_cell_by_address(self, address, cell):
        """ Set cell at position 'address' ('address' like 'A1'). """
        pos = address_to_index(address)
        return self.set_cell_by_index(pos, cell)

    def _get_index_of_first_row(self):
        first_row = self.xmlnode.find(TableRow.TAG)
        if first_row is not None:
            return self.xmlnode.index(first_row)
        else:
            return 0

    def _get_row_at_index(self, index):
        first_row_index = self._get_index_of_first_row()
        return self.xmlnode[first_row_index+index]

    def row(self, index):
        if isinstance(index, str):
            index, column = address_to_index(index)
        if index < 0:
            raise IndexError('row index out of range: %s' % index)
        return ( self._wrap((index, col), xmlnode) for col, xmlnode in enumerate(self._get_row_at_index(index)) )

    def column(self, index):
        if isinstance(index, str):
            row, index = address_to_index(index)
        if index < 0 or index >= self.ncols():
            raise IndexError('row index out of range: %s' % index)
        return ( self._wrap((xrow,index), row[index]) for xrow, row in enumerate(self.xmlnode.findall(TableRow.TAG)) )

@register_class
class TableRow(GenericWrapper, _StylenNameMixin, _VisibilityMixin,
               _DefaultCellStyleNameMixin):
    TAG = CN('table:table-row')

    def __init__(self, ncols=10, xmlnode=None):
        super(TableRow, self).__init__(xmlnode=xmlnode)
        if xmlnode is None:
            self._setup(ncols)

    def _setup(self, ncols):
        for col in range(ncols):
            self.append(Cell())

    @property
    def rows_repeated(self):
        value = self.get_attr(CN('table:number-rows-repeated'))
        value = int(value) if value is not None else 1
        return max(1, value)

    def clear_rows_repeated(self):
        del self.xmlnode.attrib[CN('table:number-rows-repeated')]

@register_class
class TableColumn(GenericWrapper, _StylenNameMixin, _VisibilityMixin,
                  _DefaultCellStyleNameMixin, _NumberColumnsRepeatedMixin):
    TAG = CN('table:table-column')


VALID_VALUE_TYPES = frozenset( ('float', 'percentage', 'currency', 'date', 'time',
                                'boolean', 'string') )
NUMERIC_TYPES = frozenset( ('float', 'percentage', 'currency') )

TYPE_VALUE_MAP = {
    'string': CN('office:string-value'),
    'float': CN('office:value'),
    'percentage': CN('office:value'),
    'currency': CN('office:value'),
    'date': CN('office:date-value'),
    'time': CN('office:time-value'),
    'boolean': CN('office:boolean-value'),
}

# These Classes are supported to read their plaintext content from the
# cell-content.
SUPPORTED_CELL_CONTENT = ("Paragraph", "Heading")

@register_class
class Cell(GenericWrapper, _StylenNameMixin, _NumberColumnsRepeatedMixin):
    CELL_ONLY_ATTRIBS = (CN('table:number-rows-spanned'),
                         CN('table:number-columns-spanned'),
                         CN('table:number-matrix-columns-spanned'),
                         CN('table:number-matrix-rows-spanned'))

    TAG = CN('table:table-cell')

    def __init__(self, value=None, value_type=None, style_name=None, xmlnode=None):
        super(Cell, self).__init__(xmlnode=xmlnode)
        if xmlnode is None:
            if style_name is not None:
                self.style_name = style_name
            if value is not None:
                self.set_value(value, value_type)
            elif value_type is not None:
                self._set_value_type(value_type)

    @property
    def content_validation_name(self):
        return self.get_attr(CN('table:content-validation-name'))
    @content_validation_name.setter
    def content_validation_name(self, value):
        self.set_attr(CN('table:content-validation-name'), value)

    @property
    def formula(self):
        return self.get_attr(CN('table:formula'))
    @formula.setter
    def formula(self, value):
        self.set_attr(CN('table:formula'), value)

    @property
    def value_type(self):
        return self.get_attr(CN('office:value-type'))

    @property
    def value(self):
        try:
            return self._value
        except AttributeError:
            pass
        t = self.value_type
        if  t is None:
            return None
        elif t == 'string':
            result = self.plaintext()
        else:
            result = self.get_attr(TYPE_VALUE_MAP[t])
            if result is None:
                pass
            elif t in NUMERIC_TYPES:
                result = float(result)
            elif t == 'boolean':
                result = True if result == 'true' else False
        self._set_cached_value(result)
        return result

    def set_value(self, value, value_type=None, currency=None):

        def is_valid_value(value):
            result = True
            if value is None:
                result = False
            elif isinstance(value, GenericWrapper):
                if value.kind not in SUPPORTED_CELL_CONTENT:
                    result = False
            return result

        def is_valid_type(value_type):
            return True if value_type in VALID_VALUE_TYPES else False

        def determine_value_type(value):
            if type(value) == bool:
                value_type = 'boolean'
            elif isinstance(value, (float, int)):
                value_type = 'float'
            else:
                value_type = 'string'
            return value_type

        def convert(value, value_type):
            if isinstance(value, GenericWrapper):
                pass
            elif value_type == 'string':
                value = Paragraph(str(value))
            elif value_type == 'boolean':
                value = 'true' if value else 'false'
            else:
                value = str(value)
            return value

        if not is_valid_value(value):
            raise ValueError("invalid value: %s" % str(value))
        if isinstance(currency, str):
            value_type = 'currency'
        if value_type is None:
            value_type = determine_value_type(value)
        if not is_valid_type(value_type):
            raise TypeError(value_type)

        value = convert(value, value_type)
        self._clear_old_value()
        self._set_new_value(value, value_type, currency)

    def _set_new_value(self, value, value_type, currency):
        if isinstance(value, GenericWrapper):
            value_type = 'string'
            self.append(value)
        else:
            self.set_attr(TYPE_VALUE_MAP[value_type], value)
        self._set_value_type(value_type)

        if currency and (value_type == 'currency'):
            self.set_attr(CN('office:currency'), currency)

    def _set_value_type(self, value_type):
        self.set_attr(CN('office:value-type'), value_type)

    def _clear_old_value(self):
        self._clear_value_attribute(self.value_type)
        self._clear_content()
        self._delete_cached_value()

    def _clear_content(self):
        xmlnode = self.xmlnode
        while len(xmlnode) > 0:
            del xmlnode[0]

    def _clear_value_attribute(self, value_type):
        try:
            attribute_name = TYPE_VALUE_MAP[value_type]
            del self.xmlnode.attrib[attribute_name]
        except KeyError:
            pass

    def _delete_cached_value(self):
        if hasattr(self, '_value'):
            del self._value

    def _set_cached_value(self, value):
        self._value = value

    @property
    def display_form(self):
        return self.plaintext()
    @display_form.setter
    def display_form(self, text):
        t = self.value_type
        if t is None or t == 'string':
            raise TypeError("not supported for value type 'None' and  'string'")
        display_form = Paragraph(text)
        first_paragraph = self.find(Paragraph.TAG)
        if first_paragraph is None:
            self.append(display_form)
        else:
            self.replace(first_paragraph, display_form)

    def plaintext(self):
        return "\n".join([p.plaintext() for p in iter(self)
                          if p.kind in SUPPORTED_CELL_CONTENT])

    def append_text(self, text, style_name=None):
        if self.value_type != 'string':
            raise TypeError('invalid cell type: %s' % self.value_type)
        try:
            last_child = self.get_child(-1)
            if last_child.kind in ("Paragraph", "Heading"):
                last_child.append(Span(text, style_name=style_name))
                return
        except IndexError:
            pass
        self.append(Paragraph(text, style_name=style_name))

    @property
    def currency(self):
        return self.get_attr(CN('office:currency'))

    @property
    def protected(self):
        return self.get_bool_attr(CN('table:protect'))
    @protected.setter
    def protected(self, value):
        self.set_bool_attr(CN('table:protect'), value)

    @property
    def span(self):
        rows = self.get_attr(CN('table:number-rows-spanned'))
        cols = self.get_attr(CN('table:number-columns-spanned'))
        rows = 1 if rows is None else max(1, int(rows))
        cols = 1 if cols is None else max(1, int(cols))
        return (rows, cols)
    @span.setter
    def span(self, value):
        rows, cols = value
        rows = max(1, int(rows))
        cols = max(1, int(cols))
        self.set_attr(CN('table:number-rows-spanned'), str(rows))
        self.set_attr(CN('table:number-columns-spanned'), str(cols))

    @property
    def covered(self):
        return self.xmlnode.tag == CN('table:covered-table-cell')
    @covered.setter
    def covered(self, value):
        if value:
            self.TAG = CN('table:covered-table-cell')
            self.xmlnode.tag = self.TAG
            self._remove_exclusive_cell_attributes()
        else:
            self.TAG = CN('table:table-cell')
            self.xmlnode.tag = self.TAG

    def _remove_exclusive_cell_attributes(self):
        for key in self.CELL_ONLY_ATTRIBS:
            if key in self.xmlnode.attrib:
                del self.xmlnode.attrib[key]

@register_class
class CoveredCell(Cell):
    TAG = CN('table:covered-table-cell')

    @property
    def kind(self):
        return 'Cell'
