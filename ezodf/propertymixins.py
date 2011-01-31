#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: property mixins
# Created: 30.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import CN

class TableStylenNameMixin:
    @property
    def style_name(self):
        return self.get_attr(CN('table:style-name'))
    @style_name.setter
    def style_name(self, name):
        self.set_attr(CN('table:style-name'), name)

class TableDefaultCellStyleNameMixin:
    @property
    def default_cell_style_name(self):
        return self.get_attr(CN('table:default-cell-style-name'))
    @default_cell_style_name.setter
    def default_cell_style_name(self, value):
        self.set_attr(CN('table:default-cell-style-name'), value)

class TableVisibilityMixin:
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

class TableNumberColumnsRepeatedMixin:
    @property
    def columns_repeated(self):
        value = self.get_attr(CN('table:number-columns-repeated'))
        value = int(value) if value is not None else 1
        return max(1, value)
    def clear_columns_repeated_attribute(self):
        del self.xmlnode.attrib[CN('table:number-columns-repeated')]
