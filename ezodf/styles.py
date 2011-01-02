#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF styles.xml document management
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from functools import partial

from .const import STYLES_NSMAP
from .xmlns import XML

## file 'styles.xml'

class Styles:
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
        pass

## style container

class Container:
    def __init__(self, xmlcontainer):
        if xmlcontainer.tag not in self.ROOTNAMES:
            raise TypeError('Unexpected root element: %s' % xmlcontainer.tag)
        self.xmlcontainer = xmlcontainer
        self._cache = {}

    def __getitem__(self, key):
        style = self._find(key)
        if style is not None:
            try: # to wrap the style element into a Python object
                return STYLEOBJECTS[style.tag](style)
            except KeyError:
                raise TypeError('Unknown style element: %s (contact ezodf developer)' % style.tag)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if XML.etree.iselement(value):
            style = self._find(key)
            if style is None:
                self.xmlcontainer.append(value)
            else:
                self.xmlcontainer.replace(style, value)
            self._cache[key] = value
        else:
            raise TypeError(str(type(value)))

    def _find(self, name):
        try:
            return self._cache[name]
        except KeyError:
            for style in self.xmlcontainer.iterchildren():
                stylename = style.get(XML('style:name'))
                if stylename == name:
                    self._cache[name] = style
                    return style
        return None

class FontFaceContainer(Container):
    ROOTNAMES = frozenset([XML('office:font-face-decls'),])

class StyleContainer(Container):
    ROOTNAMES = frozenset([XML('office:styles'),
                           XML('office:automatic-styles'),
                           XML('office:master-styles')])

## style objects

class BaseStyle:
    def __init__(self, xmlelement):
        self.xmlelement = xmlelement

    def _getattr(self, cn_name):
        element = self_get_element(cn_name)
        attr = element.get(cn_name)
        return attr if attr is not None else ""

    def _setattr(self, value, cn_name):
        element = self_get_element(cn_name)
        self.xmlelement.set(cn_name, value)

    name = property(fget = partial(self._getattr(name=XML('style:name'))),
                   fset = partial(self._setattr(name=XML('style:name'))),
                   doc = "style:name")

    def _get_element(self, cn_name):
        return self.xmlelement

class Style(BaseStyle):
    pass

class FontFace(BaseStyle):
    pass

STYLEOBJECTS = {
    XML('style:style'): Style,
    XML('style:font-face'): FontFace,
}
