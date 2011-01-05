#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: text objects
# Created: 03.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import CN, XML
from .base import BaseClass

class Spaces(BaseClass):
    TAG = CN('text:s')
    def __init__(self, count=1, xmlroot=None):
        super(Spaces, self).__init__(xmlroot)
        if xmlroot is None:
            self._set_count(count)

    def _get_count(self):
        count = self.getattr(CN('text:c'))
        return int(count) if count is not None else 1
    def _set_count(self, value):
        self.setattr(CN('text:c'), str(value))
    count = property(_get_count, _set_count)

    def plaintext(self):
        return ' ' * self.count

XML.register_class(Spaces)

class Tabulator(BaseClass):
    TAG = CN('text:t')
    def plaintext(self):
        return '\t'

XML.register_class(Tabulator)

class Span(BaseClass):
    TAG = CN('text:span')
    def __init__(self, text="", xmlroot=None):
        super(Span, self).__init__(xmlroot)

    def plaintext(self):
        text = []
        if self.xmlroot.text is not None:
            text.append(self.xmlroot.text)
        for element in iter(self):
            if hasattr(element, 'plaintext'):
                text.append(element.plaintext())
        return "".join(text)

XML.register_class(Span)

class Paragraph(Span):
    TAG = CN('text:p')

XML.register_class(Paragraph)

class Heading(Span):
    TAG = CN('text:h')

XML.register_class(Heading)

class Section(BaseClass):
    TAG = CN('text:section')

XML.register_class(Section)

class List(BaseClass):
    TAG = CN('text:list')

XML.register_class(List)
