#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: text objects
# Created: 03.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import CN, register_class
from .base import BaseClass

@register_class
class Spaces(BaseClass):
    TAG = CN('text:s')
    def __init__(self, count=1, xmlroot=None):
        super(Spaces, self).__init__(xmlroot)
        if xmlroot is None:
            self.count = count
    @property
    def count(self):
        count = self.getattr(CN('text:c'))
        return int(count) if count is not None else 1
    @count.setter
    def count(self, value):
        self.setattr(CN('text:c'), str(value))

    def plaintext(self):
        return ' ' * self.count

@register_class
class Tabulator(BaseClass):
    TAG = CN('text:t')
    def plaintext(self):
        return '\t'


@register_class
class Span(BaseClass):
    TAG = CN('text:span')
    def __init__(self, text="", xmlroot=None):
        super(Span, self).__init__(xmlroot)

    def plaintext(self):
        text = [self.xmlroot.text]
        for element in iter(self):
            try:
                text.append(element.plaintext())
            except AttributeError:
                text.append(element.xmlroot.text)
            text.append(element.xmlroot.tail)
        return "".join(filter(None, text))


@register_class
class Paragraph(Span):
    TAG = CN('text:p')

@register_class
class Heading(Span):
    TAG = CN('text:h')

@register_class
class Section(BaseClass):
    TAG = CN('text:section')

@register_class
class List(BaseClass):
    TAG = CN('text:list')
