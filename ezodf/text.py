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


class _StyleNameMixin:
    @property
    def style_name(self):
        return self.get_attr(CN('text:style-name'))
    @style_name.setter
    def style_name(self, name):
        self.set_attr(CN('text:style-name'), name)


class _NumberingMixin:
    @property
    def start_value(self):
        value = self.get_attr(CN('text:start-value'))
        return int(value) if value is not None else None
    @start_value.setter
    def start_value(self, value):
        value = str(int(value))
        self.set_attr(CN('text:start-value'), value)

    @property
    def formatted_number(self):
        formatted_number = self.xmlnode.find(CN('text:number'))
        return formatted_number.text if formatted_number is not None else None
    @formatted_number.setter
    def formatted_number(self, value):
        formatted_number = subelement(self.xmlnode, CN('text:number'))
        formatted_number.text = str(value)


@register_class
class Span(GenericWrapper, _StyleNameMixin):
    TAG = CN('text:span')
    def __init__(self, text="", style_name="", xmlnode=None):
        super(Span, self).__init__(xmlnode)
        if style_name:
            self.style_name = style_name
        if text:
            self.append_text(text)

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

    @property
    def cond_style_name(self):
        return self.get_attr(CN('text:cond-style-name'))
    @cond_style_name.setter
    def cond_style_name(self, value):
        self.set_attr(CN('text:cond-style-name'), value)

    @property
    def ID(self):
        return self.get_attr(CN('text:id'))
    @ID.setter
    def ID(self, value):
        self.set_attr(CN('text:id'), value)

@register_class
class NumberedParagraph(Span):
    TAG = CN('text:numbered-paragraph')

@register_class
class Heading(Span, _NumberingMixin):
    TAG = CN('text:h')

    def __init__(self, text="", outline_level=1, style_name="", xmlnode=None):
        super(Heading, self).__init__(text, style_name, xmlnode)
        if xmlnode is None:
            self.outline_level = outline_level

    @property
    def outline_level(self):
        return int(self.get_attr(CN('text:outline-level')))
    @outline_level.setter
    def outline_level(self, level):
        number = max(int(level), 1)
        self.set_attr(CN('text:outline-level'), str(number))

    @property
    def restart_numbering(self):
        return True if self.get_attr(CN('text:restart-numbering')) == 'true' else False
    @restart_numbering.setter
    def restart_numbering(self, value):
        value = 'true' if value else 'false'
        self.set_attr(CN('text:restart-numbering'), value)

    @property
    def suppress_numbering(self):
        return True if self.get_attr(CN('text:is-list-header')) == 'true' else False
    @suppress_numbering.setter
    def suppress_numbering(self, value):
        value = 'true' if value else 'false'
        self.set_attr(CN('text:is-list-header'), value)


@register_class
class Hyperlink(Span):
    TAG = CN('text:a')

    def __init__(self, href, text="", style_name="", xmlnode=None):
        super(Hyperlink, self).__init__(text, style_name, xmlnode)
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
class ListHeader(GenericWrapper):
    TAG = CN('text:list-header')

    def __init__(self, text="", xmlnode=None):
        super(ListHeader, self).__init__(xmlnode)
        if text:
            self.append(Paragraph(text))


@register_class
class ListItem(ListHeader, _NumberingMixin):
    TAG = CN('text:list-item')


@register_class
class List(GenericWrapper, _StyleNameMixin):
    TAG = CN('text:list')

    def __init__(self, style_name="", xmlnode=None):
        super(List, self).__init__(xmlnode)
        if style_name:
            self.style_name = stylename

    @property
    def continue_numbering(self):
        return True if self.get_attr(CN('text:continue-numbering')) == 'true' else False
    @continue_numbering.setter
    def continue_numbering(self, value):
        value = 'true' if value else 'false'
        self.set_attr(CN('text:continue-numbering'), value)

    @property
    def header(self):
        return self.xmlnode.find(CN('text:list-header'))
    @header.setter
    def header(self, header):
        if header.kind != 'ListHeader':
            raise TypeError("param 'header' is not a list header.")
        oldheader = self.xmlnode.find(CN('text:list-header'))
        if oldheader:
            self.xmlnode.remove(oldheader)
        self.append(header)

    def iteritems(self):
        return self.findall(CN('text:list-item'))


@register_class
class Section(GenericWrapper):
    TAG = CN('text:section')
