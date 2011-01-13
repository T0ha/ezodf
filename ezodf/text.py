#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: text objects
# Created: 03.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import CN, register_class, subelement
from .base import GenericWrapper, safelen
from .whitespaces import encode_whitespaces


@register_class
class Span(GenericWrapper):
    TAG = CN('text:span')
    def __init__(self, text="", stylename="", xmlnode=None):
        super(Span, self).__init__(xmlnode)
        if stylename:
            self.stylename = stylename
        if text:
            self.append_plaintext(text)

    @property
    def style_name(self):
        return self.get_attr(CN('text:style-name'))
    @style_name.setter
    def style_name(self, name):
        self.set_attr(CN('text:style-name'), name)

    @property
    def textlen(self):
        # NOTE: do not cache this value before you can guarantee that
        # you detect ALL text changes in this node and all of it child nodes.
        length = safelen(self.xmlnode.text)
        for element in iter(self):
            length += (element.textlen + safelen(element.xmlnode.tail))
        return length

    def plaintext(self):
        # NOTE: do not cache this value before you can guarantee that
        # you detect ALL text changes in this node and all of it child nodes.
        text = [self.xmlnode.text]
        for element in iter(self):
            text.append(element.plaintext())
            text.append(element.xmlnode.tail)
        return "".join(filter(None, text))

    def append_plaintext(self, text):
        def append(text, new):
            return text + new if text else new

        for tag in encode_whitespaces(text):
            if isinstance(tag, str):
                if len(self.xmlnode) > 0:
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

    def __init__(self, text="", outline_level=1, stylename=None, xmlnode=None):
        super(Heading, self).__init__(text, stylename, xmlnode)
        self.outline_level = outline_level

    @property
    def outline_level(self):
        return int(self.get_attr(CN('text:outline-level')))

    @outline_level.setter
    def outline_level(self, level):
        self.set_attr(CN('text:outline-level'), str(int(level)))


@register_class
class Section(GenericWrapper):
    TAG = CN('text:section')


@register_class
class List(GenericWrapper):
    TAG = CN('text:list')
