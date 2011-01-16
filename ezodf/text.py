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
            self.append_text(text)

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

    def append_text(self, text):
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
                self.append(tag)

@register_class
class Paragraph(Span):
    TAG = CN('text:p')

@register_class
class Heading(Span):
    TAG = CN('text:h')

    def __init__(self, text="", outline_level=1, stylename="", xmlnode=None):
        super(Heading, self).__init__(text, stylename, xmlnode)
        if xmlnode is None:
            self.outline_level = outline_level

    @property
    def outline_level(self):
        return int(self.get_attr(CN('text:outline-level')))

    @outline_level.setter
    def outline_level(self, level):
        number = max(int(level), 1)
        self.set_attr(CN('text:outline-level'), str(number))

@register_class
class Hyperlink(Paragraph):
    TAG = CN('text:a')

    def __init__(self, href, text="", stylename="", xmlnode=None):
        super(Hyperlink, self).__init__(text, stylename, xmlnode)
        self.href = href
        self.target_frame = '_blank'

    @property
    def name(self):
        return self.get_attr(CN('office:name'))
    @name.setter
    def name(self, name):
        self.set_attr(CN('office:name'), name)

    @property
    def href(self):
        return self.get_attr(CN('xlink:href'))
    @href.setter
    def href(self, href):
        self.set_attr(CN('xlink:href'), href)

    @property
    def target_frame(self):
        return self.get_attr(CN('office:target-frame-name'))
    @target_frame.setter
    def target_frame(self, framename):
        self.set_attr(CN('office:target-frame-name'), framename)
        show = 'new' if framename == '_blank' else 'replace'
        self.set_attr(CN('xlink:show'), show)

@register_class
class Section(GenericWrapper):
    TAG = CN('text:section')


@register_class
class List(GenericWrapper):
    TAG = CN('text:list')
