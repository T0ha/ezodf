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
class SimpleVariables(GenericWrapper):  # {{{1
    TAG = CN('text:variable-decls')
    variables = {}

    def __init__(self, xmlnode=None):  # {{{2
        """docstring for __init__"""
        super(SimpleVariables, self).__init__(xmlnode)
        for v in self:
            self.variables[v.name] = v

    def __getitem__(self, index):  # {{{2
        if index in self.variables:
            return self.variables[index]
        else:
            return self.get_child(index)

    def __setitem__(self, index, value):  # {{{2
        if index in self.variables:
            self.variables[index].value = value
        else:
            return self.set_child(index, value)


@register_class
class SimpleVariable(GenericWrapper):  # {{{1
    TAG = CN('text:variable-decl')

    def __init__(self, xmlnode=None):  # {{{2
        """docstring for __init__"""
        super(SimpleVariable, self).__init__(xmlnode)
        self.name = self.xmlnode.get(CN('text:name'))
        self.instances = []

    @property
    def value(self):  # {{{2
        """
        Get variable value
        FIXME: (it's assumed that all instances have the same value)
        """
        return self.instances[0].value

    @value.setter
    def value(self, v):  # {{{2
        """
        Set variable value
        """
        vtype = type(v)

        for instance in self.instances:
            instance.value = v

        if vtype == bool:
            self.type = u'boolean'
        elif vtype == int or vtype == float:
            self.type = u'float'
        else:
            self.type = u'string'

    @property
    def type(self):  # {{{2
        """Gets type of variable"""
        return self.get_attr(CN('office:value-type'), u'string')

    @type.setter
    def type(self, t):  # {{{2
        """Sets type of variable"""
        self.set_attr(CN('office:value-type'), unicode(t))


@register_class
class SimpleVariableInstance(GenericWrapper):  # {{{1
    TAG = CN('text:variable-set')

    def __init__(self, xmlnode=None):  # {{{2
        super(SimpleVariableInstance, self).__init__(xmlnode)
        self.name = self.xmlnode.get(CN('text:name'))
        try:
            SimpleVariables.variables[self.name].instances.append(self)
        except KeyError:
            pass

    @property
    def value(self):  # {{{2
        """Gets instavce value"""
        if self.type == u'string':
            return self.text
        elif self.type == u'boolean':
            return self.text == 'true'
        elif self.type == u'float':
            return float(self.text)
        else:
            return self.text

    @value.setter
    def value(self, v):  # {{{2
        """Sets instavce value"""

        vtype = type(v)
        self.text = unicode(v)
        if vtype == bool:
            self.type = u'boolean'
        elif vtype == int or vtype == float:
            self.type = u'float'
        else:
            self.type = u'string'

    @property
    def type(self):  # {{{2
        """Gets type of variable"""
        return self.get_attr(CN('office:value-type'), u'string')

    @type.setter
    def type(self, t):  # {{{2
        """Sets type of variable"""
        self.set_attr(CN('office:value-type'), unicode(t))

