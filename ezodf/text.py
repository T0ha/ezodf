#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: text objects
# Created: 03.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import CN, register_class, subelement
from .base import BaseClass, safelen

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

    @property
    def textlen(self):
        return self.count

    def plaintext(self):
        return ' ' * self.count

@register_class
class Tabulator(BaseClass):
    TAG = CN('text:tab')

    @property
    def textlen(self):
        return 1

    def plaintext(self):
        return '\t'

@register_class
class LineBreak(BaseClass):
    TAG = CN('text:line-break')

    @property
    def textlen(self):
        return 1

    def plaintext(self):
        return '\n'


@register_class
class Span(BaseClass):
    TAG = CN('text:span')
    def __init__(self, text="", stylename=None, xmlroot=None):
        super(Span, self).__init__(xmlroot)
        if (xmlroot is None) and (stylename is not None):
            self.stylename = stylename

    @property
    def stylename(self):
        return self.getattr(CN('text:style-name'))
    @stylename.setter
    def stylename(self, name):
        self.setattr(CN('text:style-name'), name)

    @property
    def textlen(self):
        # NOTE: do not cache this value before you can guarantee that
        # you detect ALL text changes in this node and all of it child nodes.
        length = safelen(self.xmlroot.text)
        for element in iter(self):
            length += (element.textlen + safelen(element.xmlroot.tail))
        return length

    def plaintext(self):
        # NOTE: do not cache this value before you can guarantee that
        # you detect ALL text changes in this node and all of it child nodes.
        text = [self.xmlroot.text]
        for element in iter(self):
            text.append(element.plaintext())
            text.append(element.xmlroot.tail)
        return "".join(filter(None, text))

@register_class
class Paragraph(Span):
    TAG = CN('text:p')

    @property
    def textlen(self):
        return super(Paragraph, self).textlen + 1

    def plaintext(self):
        return super(Paragraph, self).plaintext() + '\n'


@register_class
class Heading(Paragraph):
    TAG = CN('text:h')

    @property
    def textlevel(self):
        return int(self.getattr(CN('text:level')))

    @textlevel.setter
    def textlevel(self, level):
        self.setattr(CN('text:level'), str(int(level)))

@register_class
class Section(BaseClass):
    TAG = CN('text:section')

@register_class
class List(BaseClass):
    TAG = CN('text:list')
