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
    # Span(xmlroot=node)
    def __init__(self, text="", style=None, xmlroot=None):
        super(Span, self).__init__(xmlroot)

XML.register_class(Span)

class Paragraph(BaseClass):
    TAG = XML('text:p')
    def __init__(self, text="", style=None, xmlroot=None):
        super(Paragraph, self).__init__(xmlroot)

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
