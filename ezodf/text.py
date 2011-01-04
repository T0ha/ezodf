#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: text objects
# Created: 03.01.2011
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .xmlns import XML
from .base import BaseClass

class Span(BaseClass):
    TAG = XML('text:span')

XML.register_class(Span)

class Paragraph(BaseClass):
    TAG = XML('text:p')

    def appendtext(self, text, style=None):
        pass

XML.register_class(Paragraph)

class Heading(Paragraph):
    TAG = XML('text:h')

XML.register_class(Heading)

class Section(BaseClass):
    TAG = XML('text:section')

XML.register_class(Section)

class List(BaseClass):
    TAG = XML('text:list')

XML.register_class(List)
