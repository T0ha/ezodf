#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF styles.xml document management
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .const import STYLES_NSMAP
from .xmlns import XMLMixin, subelement, etree, CN, register_class, pyobj

## file 'styles.xml'

@register_class
class OfficeDocumentStyles(XMLMixin):
    TAG = CN('office:document-styles')

    def __init__(self, xmlroot=None):
        if xmlroot is None:
            self.xmlroot = etree.Element(self.TAG, nsmap=STYLES_NSMAP)
        elif xmlroot.tag == self.TAG:
            self.xmlroot = xmlroot
        else:
            raise ValueError("Unexpected root node: %s" % content.tag)
        self.setup()

    def setup(self):
        self.fonts = pyobj(subelement(self.xmlroot, CN('office:font-face-decls')))
        self.styles = pyobj(subelement(self.xmlroot, CN('office:styles')))
        self.automatic_styles = pyobj(subelement(self.xmlroot, CN('office:automatic-styles')))
        self.master_styles = pyobj(subelement(self.xmlroot, CN('office:master-styles')))


## style container

class Container:
    def __init__(self, xmlroot):
        assert xmlroot.tag == self.TAG
        self.xmlroot = xmlroot
        self._cache = {}

    def __getitem__(self, key):
        style = self._find(key) # by style:name attribute
        if style is not None:
            try: # to wrap the style element into a Python object
                return pyobj(style)(style)
            except KeyError:
                raise TypeError('Unknown style element: %s (contact ezodf developer)' % style.tag)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if etree.iselement(value):
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
                stylename = style.get(CN('style:name'))
                if stylename == name:
                    self._cache[name] = style
                    return style
        return None

@register_class
class OfficeFontFaceDecls(Container):
    TAG = CN('office:font-face-decls')

@register_class
class OfficeStyles(Container):
    TAG = CN('office:styles')

@register_class
class OfficeAutomaticStyles(Container):
    TAG = CN('office:automatic-styles')

@register_class
class OfficeMasterStyles(Container):
    TAG = CN('office:master-styles')

## style objects


class BaseStyle:
    ATTRIBUTEMAP = {}

    def __init__(self, xmlroot):
        self.xmlroot = xmlroot

    def __getitem__(self, key):
        """ Get style attribute 'key'. """

    def __setitem__(self, key, value):
        """ Set style attribute 'key' to 'value'. """

    def _properties(self, key, property_factory, new=True):
        """ Get or create a properties element. """
        element = subelement(self.xmlroot, key , new)
        if element is None:
            raise KeyError(key)
        propertiesname = key + '-properties'
        properties = element.find(propertiesname)
        if properties is None:
            properties = etree.SubElement(element, propertiesname)
        return property_factory(properties)

class Properties(BaseStyle):
    ATTRIBUTEMAP = {} # should contain all possible property names
    pass

HeaderProperties = Properties

@register_class
class Style(BaseStyle):
    TAG = CN('style:style')
    ATTRIBUTEMAP = {
        'name': CN('style:name'),
        'display-name': CN('style:disply-name'),
        'family': CN('style:family'),
        'parent-style-name': CN('style:parent-style-name'),
        'next-style-name': CN('style:next-style-name'),
        'list-style-name': CN('style:list-style-name'),
        'master-page-name': CN('style:master-page-name'),
        'auto-update': CN('style:auto-update'), # 'true' or 'false'
        'data-style-name': CN('style:data-style-name'),
        'class': CN('style:class'),
        'default-outline-level': CN('style:default-outline-level'),
    }

@register_class
class DefaultStyle(BaseStyle):
    TAG = CN('style:default-style')
    ATTRIBUTEMAP = {
        'family': CN('style:family'),
    }

@register_class
class PageLayout(BaseStyle):
    TAG = CN('style:page-layout')
    ATTRIBUTEMAP = {
        'name': CN('style:name'),
        'page-usage': CN('style:page-usage'), # all | left | right | mirrored
    }
    def __init__(self, xmlelement):
        super(PageLayout, self).__init__(xmlelement)
        self.header = self._properties(CN('style:header-style'), HeaderProperties)
        self.footer = self._properties(CN('style:footer-style'), HeaderProperties)

@register_class
class FontFace(BaseStyle):
    TAG = CN('style:font-face')


