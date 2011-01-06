#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: text objects
# Created: 03.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from array import array

from .xmlns import CN, register_class, subelement
from .base import BaseClass, safelen
from .textprocessing import encode


@register_class
class Span(BaseClass):
    TAG = CN('text:span')
    def __init__(self, text="", stylename=None, xmlroot=None):
        super(Span, self).__init__(xmlroot)
        if (xmlroot is None) and (stylename is not None):
            self.stylename = stylename
        if text:
            self.append_plaintext(text)

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

    def append_plaintext(self, text):
        def append(text, new):
            return text + new if text else new

        for tag in encode(text):
            if isinstance(tag, str):
                if len(self.xmlroot) > 0:
                    lastchild = self[-1]
                    lastchild.tail = append(lastchild.tail, tag)
                else:
                    self.text = append(self.text, tag)
            else:
                self.add(tag)

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
