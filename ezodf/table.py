#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: table objects
# Created: 03.01.2011
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .xmlns import register_class, CN
from .base import GenericWrapper
from .protection import random_protection_key

@register_class
class Table(GenericWrapper):
    TAG = CN('table:table')

    @property
    def name(self):
        return self.get_attr(CN('table:name'))
    @name.setter
    def name(self, value):
        return self.set_attr(CN('table:name'), value)

    @property
    def style_name(self):
        return self.get_attr(CN('table:style-name'))
    @style_name.setter
    def style_name(self, name):
        self.set_attr(CN('table:style-name'), name)

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