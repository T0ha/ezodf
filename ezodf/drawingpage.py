#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: Page Class
# Created: 12.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import CN, register_class
from .base import GenericWrapper

@register_class
class DrawingPage(GenericWrapper):
    TAG = CN('draw:page')

    def __init__(self, name="", xmlnode=None):
        super(DrawingPage, self).__init__(xmlnode)
        if xmlnode is None:
            self.name = name
            self._setup()

    def _setup(self):
        pass

    @property
    def name(self):
        return self.get_attr(CN('draw:name'))
    @name.setter
    def name(self, name):
        self.set_attr(CN('draw:name'), name)
