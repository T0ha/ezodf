#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: property mixins
# Created: 30.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import CN, subelement

class TextNumberingMixin:
    @property
    def start_value(self):
        value = self.get_attr(CN('text:start-value'))
        return int(value) if value is not None else None
    @start_value.setter
    def start_value(self, value):
        value = str(max(int(value), 1))
        self.set_attr(CN('text:start-value'), value)

    @property
    def formatted_number(self):
        formatted_number = self.xmlnode.find(CN('text:number'))
        return formatted_number.text if formatted_number is not None else None
    @formatted_number.setter
    def formatted_number(self, value):
        formatted_number = subelement(self.xmlnode, CN('text:number'))
        formatted_number.text = str(value)

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

def StringProperty(name, doc=None):
    def getter(self):
        return self.xmlnode.get(name)
    def setter(self, value):
        self.xmlnode.set(name, value)
    def deleter(self):
        del self.xmlnode.attrib[name]
    return property(getter, setter, deleter, doc)

def BooleanProperty(name, doc=None):
    def getter(self):
        return self.xmlnode.get(name) == 'true'
    def setter(self, value):
        value = 'true' if value else 'false'
        self.xmlnode.set(name, value)
    def deleter(self):
        del self.xmlnode.attrib[name]
    return property(getter, setter, deleter, doc)

def FloatProperty(name, doc=None):
    def getter(self):
        value = self.xmlnode.get(name)
        if value is None:
            return None
        else:
            return float(value)
    def setter(self, value):
        self.xmlnode.set(name, str(value))
    def deleter(self):
        del self.xmlnode.attrib[name]
    return property(getter, setter, deleter, doc)

def IntegerProperty(name, doc=None):
    def getter(self):
        value = self.xmlnode.get(name)
        if value is None:
            return None
        else:
            return int(value)
    def setter(self, value):
        self.xmlnode.set(name, str(value))
    def deleter(self):
        del self.xmlnode.attrib[name]
    return property(getter, setter, deleter, doc)

def IntegerWithLowerLimitProperty(name, lower_limit=0, doc=None):
    def getter(self):
        value = self.xmlnode.get(name)
        if value is None:
            return lower_limit
        else:
            return max(lower_limit, int(value))
    def setter(self, value):
        value = int(value)
        self.xmlnode.set(name, str(max(lower_limit, value)))
    def deleter(self):
        del self.xmlnode.attrib[name]
    return property(getter, setter, deleter, doc)
