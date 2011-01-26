#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: table objects
# Created: 03.01.2011
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .xmlns import register_class, CN, wrap
from .base import GenericWrapper
from .protection import random_protection_key


class _StylenameMixin:
    @property
    def style_name(self):
        return self.get_attr(CN('table:style-name'))
    @style_name.setter
    def style_name(self, name):
        self.set_attr(CN('table:style-name'), name)


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

class _DefaultStyleNameMixin:
    @property
    def default_cell_style_name(self):
        return self.get_attr(CN('table:default-cell-style-name'))
    @default_cell_style_name.setter
    def default_cell_style_name(self, value):
        self.set_attr(CN('table:default-cell-style-name'), value)

@register_class
class Table(GenericWrapper, _StylenameMixin):
    TAG = CN('table:table')

    def __init__(self, name='NEWTABLE', size=(10, 10), xmlnode=None):
        super(Table, self).__init__(xmlnode=xmlnode)
        self._cell_cache = {}
        if xmlnode is None:
            self.name = name
            self._setup(size[0], size[1])

    def _setup(self, nrows, ncols):
        for row in range(nrows):
            self.append(TableRow(ncols=ncols))
        self._reset_cache()

    def _reset_cache(self):
        self._cell_cache.clear()

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
        # it's a method to shows that a call is expensive
        count = 0
        for row in self.findall(CN('table:table-row')):
            count += row.rows_repeated
        return count

    def ncols(self):
        """ Count of table columns. """
        # it's a method to shows that a call is expensive
        first_row = self.find(CN('table:table-row'))
        count = 0
        if first_row is not None:
            for cell in first_row:
                count += cell.columns_repeated
        return count

    def get_cell(self, row, col):
        return TableCell()

@register_class
class TableRow(GenericWrapper, _StylenameMixin, _VisibilityMixin,
               _DefaultStyleNameMixin):
    TAG = CN('table:table-row')

    def __init__(self, ncols=10, xmlnode=None):
        super(TableRow, self).__init__(xmlnode=xmlnode)
        if xmlnode is None:
            self._setup(ncols)

    def _setup(self, ncols):
        for col in range(ncols):
            self.append(TableCell())

    @property
    def rows_repeated(self):
        value = self.get_attr(CN('table:number-rows-repeated'))
        value = int(value) if value is not None else 1
        return max(1, value)
    @rows_repeated.setter
    def rows_repeated(self, value):
        value = int(value)
        if value < 1:
            raise ValueError("Number rows repeated should >= 1.")
        self.set_attr(CN('table:number-rows-repeated'), str(value))

@register_class
class TableColumn(GenericWrapper, _StylenameMixin, _VisibilityMixin,
                  _DefaultStyleNameMixin):
    TAG = CN('table:table-column')

    @property
    def cols_repeated(self):
        value = self.get_attr(CN('table:number-columns-repeated'))
        value = int(value) if value is not None else 1
        return max(1, value)
    @cols_repeated.setter
    def cols_repeated(self, value):
        value = int(value)
        if value < 1:
            raise ValueError("Number cols repeated should >= 1.")
        self.set_attr(CN('table:number-columns-repeated'), str(value))

VALID_VALUE_TYPES = frozenset( ('float', 'percentage', 'currency', 'date', 'time',
                                'boolean', 'string') )
TYPE_VALUE_MAP = {
    'string': CN('office:string-value'),
    'float': CN('office:value'),
    'percentage': CN('office:value'),
    'currency': CN('office:value'),
    'date': CN('office:date-value'),
    'time': CN('office:time-value'),
    'boolean': CN('office:boolean-value'),
}

@register_class
class CoveredTableCell(GenericWrapper, _StylenameMixin):
    TAG = CN('table:covered-table-cell')

    @property
    def columns_repeated(self):
        value = self.get_attr(CN('table:number-columns-repeated'))
        value = int(value) if value is not None else 1
        return max(1, value)

    @columns_repeated.setter
    def columns_repeated(self, value):
        value = int(value)
        if value < 1:
            raise ValueError("Number columns repeated should >= 1.")
        self.set_attr(CN('table:number-columns-repeated'), str(value))

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
        return self.get_attr(CN('table:value-type'))
    @value_type.setter
    def value_type(self, value):
        if value not in VALID_VALUE_TYPES:
            raise ValueError(str(value))
        self.set_attr(CN('table:value-type'), value)

    @property
    def current_value(self):
        t = self.value_type
        if  t is None:
            return None
        else:
            tag = TYPE_VALUE_MAP[t]
            return self.get_attr(tag)
    @current_value.setter
    def current_value(self, value):
        t = self.value_type
        if t is None:
            self.value_type = t = 'string'
        self.set_attr(TYPE_VALUE_MAP[t], str(value))

    def set_current_value(self, current_value, value_type):
        self.value_type = value_type
        self.current_value = current_value

    @property
    def currency(self):
        return self.get_attr(CN('office:currency'))
    @currency.setter
    def currency(self, value):
        self.value_type = 'currency'
        self.set_attr(CN('office:currency'), value)

    @property
    def protected(self):
        return self.get_bool_attr(CN('table:protect'))
    @protected.setter
    def protected(self, value):
        self.set_bool_attr(CN('table:protect'), value)

@register_class
class TableCell(CoveredTableCell):
    TAG = CN('table:table-cell')

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
