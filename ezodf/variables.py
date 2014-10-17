#!/usr/bin/env python
#coding:utf-8
# Purpose: variables and user_fields objects
# Created: 10.10.2014
# Copyright (C) 2014, Shvein Anton
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "T0ha <t0hashvein@gmail.com>"

from .xmlns import register_class, CN
from .base import GenericWrapper


@register_class
class SimpleVariables(GenericWrapper):
    TAG = CN('text:variable-decls')
    variables = {}

    def __init__(self, xmlnode=None):
        """docstring for __init__"""
        super(SimpleVariables, self).__init__(xmlnode)
        for v in self:
            self.variables[v.name] = v

    def __getitem__(self, index):
        if index in self.variables:
            return self.variables[index]
        else:
            return self.get_child(index)

    def __setitem__(self, index, value):
        if index in self.variables:
            self.variables[index].set(value)
        else:
            return self.set_child(index)


@register_class
class SimpleVariable(GenericWrapper):
    TAG = CN('text:variable-decl')

    def __init__(self, xmlnode=None):
        """docstring for __init__"""
        super(SimpleVariable, self).__init__(xmlnode)
        self.name = self.xmlnode.get(CN('text:name'))
        self.type = self.xmlnode.get(CN('text:value-type'))


