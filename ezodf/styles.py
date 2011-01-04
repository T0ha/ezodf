#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF styles.xml document management
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .const import STYLES_NSMAP
from .xmlns import XML, XMLMixin, subelement

## file 'styles.xml'

class Styles(XMLMixin):
    def __init__(self, content=None):
        if content is None:
            self.xmlroot = XML.etree.Element(XML('office:document-styles'),
                                             nsmap=STYLES_NSMAP)
            self.setup()
        else:
            if isinstance(content, bytes):
                self.xmlroot = XML.etree.fromstring(content)
            elif content.tag == XML('office:document-styles'):
                self.xmlroot = content
            else:
                raise ValueError("Unexpected root node: %s" % content.tag)

    def setup(self):
        fonts = subelement(self.xmlroot, XML('office:font-face-decls'))
        self.fonts = FontFaceDecls(fonts)

        styles = subelement(self.xmlroot, XML('office:styles'))
        self.styles = StyleContainer(styles)

        automatic_styles = subelement(self.xmlroot, XML('office:automatic-styles'))
        self.automatic_styles = StyleContainer(automatic_styles)

        master_styles = subelement(self.xmlroot, XML('office:master-styles'))
        self.master_styles = StyleContainer(master_styles)


## style container

class Container:
    def __init__(self, xmlroot):
        assert xmlroot.tag in self.ROOTNAMES
        self.xmlroot = xmlroot
        self._cache = {}

    def __getitem__(self, key):
        style = self._find(key) # by style:name attribute
        if style is not None:
            try: # to wrap the style element into a Python object
                return XML.to_object(style)(style)
            except KeyError:
                raise TypeError('Unknown style element: %s (contact ezodf developer)' % style.tag)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if XML.etree.iselement(value):
            style = self._find(key)
            if style is None:
                self.xmlroot.append(value)
            else:
                self.xmlroot.replace(style, value)
            self._cache[key] = value
        else:
            raise TypeError(str(type(value)))

    def _find(self, name):
        try:
            return self._cache[name]
        except KeyError:
            for style in self.xmlroot.iterchildren():
                stylename = style.get(XML('style:name'))
                if stylename == name:
                    self._cache[name] = style
                    return style
        return None

class FontFaceDecls(Container):
    ROOTNAMES = frozenset([XML('office:font-face-decls'),])

class StyleContainer(Container):
    ROOTNAMES = frozenset([XML('office:styles'),
                           XML('office:automatic-styles'),
                           XML('office:master-styles')])

## style objects


class BaseStyle:
    ATTRIBUTEMAP = {}

    def __init__(self, xmlroot):
        self.xmlroot = xmlroot

    def __getitem__(self, key):
        """ Get style attribute 'key'. """

    def __setitem__(self, key, value):
        """ Set style attribute 'key' to 'value'. """

    def _properties(self, key, property_factory, create=True):
        """ Get or create a properties element. """
        element = self.xmlroot.find(key)
        if element is None:
            if not create:
                raise KeyError(key)
            else:
                element = XML.etree.SubElement(self.xmlelement, key)
        propertiesname = key + '-properties'
        properties = element.find(propertiesname)
        if properties is None:
            properties = XML.etree.SubElement(element, propertiesname)
        return property_factory(properties)

class Properties(BaseStyle):
    ATTRIBUTEMAP = {} # should contain all possible property names
    pass

HeaderProperties = Properties

class Style(BaseStyle):
    TAG = XML('style:style')
    ATTRIBUTEMAP = {
        'name': XML('style:name'),
        'display-name': XML('style:disply-name'),
        'family': XML('style:family'),
        'parent-style-name': XML('style:parent-style-name'),
        'next-style-name': XML('style:next-style-name'),
        'list-style-name': XML('style:list-style-name'),
        'master-page-name': XML('style:master-page-name'),
        'auto-update': XML('style:auto-update'), # 'true' or 'false'
        'data-style-name': XML('style:data-style-name'),
        'class': XML('style:class'),
        'default-outline-level': XML('style:default-outline-level'),
    }

class DefaultStyle(BaseStyle):
    TAG = XML('style:default-style')
    ATTRIBUTEMAP = {
        'family': XML('style:family'),
    }

class PageLayout(BaseStyle):
    TAG = XML('style:page-layout')
    ATTRIBUTEMAP = {
        'name': XML('style:name'),
        'page-usage': XML('style:page-usage'), # all | left | right | mirrored
    }
    def __init__(self, xmlelement):
        super(PageLayout, self).__init__(xmlelement)
        self.header = self._properties(XML('style:header-style'), HeaderProperties)
        self.footer = self._properties(XML('style:footer-style'), HeaderProperties)

class FontFace(BaseStyle):
    TAG = XML('style:font-face')

XML.register_class(Style)
XML.register_class(FontFace)
XML.register_class(PageLayout)
XML.register_class(DefaultStyle)


