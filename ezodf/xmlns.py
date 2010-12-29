#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: support module to handle xml namespaces
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from lxml import etree

from .const import LibreOfficeNSMAP

class _XMLNamespaces:
    def __init__(self, namespaces, etree):
        self.prefix2uri = {}
        self.uri2prefix = {}
        self.etree = etree
        self._cache = {}
        self.update(namespaces)

    def update(self, namespaces):
        for prefix, uri in namespaces.items():
            self.register(prefix, uri)
        self._cache.clear()

    def register(self, prefix, uri):
        self.prefix2uri[prefix] = uri
        self.uri2prefix[uri] = prefix

    def __call__(self, tag):
        """ Convert tag in prefix notation into clark notation. """
        # cached calls
        try:
            return self._cache[tag]
        except KeyError:
            if tag[0] == '{': # tag is already in clark notation
                return tag
            else:
                cn = self._prefix2clark(tag)
                self._cache[tag] = cn
                return cn

    def _prefix2clark(self, tag):
        """ Convert tag in prefix notation into clark notation. """
        # uncached calls
        prefix, local = self._split_prefix(tag)
        return "{%s}%s" % (self.prefix2uri[prefix], local)

    def _split_prefix(self, tag):
        if tag.count(':') == 1:
            return tag.split(':')
        else:
            raise ValueError("prefix-notation required 'prefix:local': %s" % tag)

    def parse(self, source):
        xmlroot = self.etree.parse(soure)
        return xmlroot

    def fromstring(self, text):
        xmlroot = self.etree.fromstring(text)
        return xmlroot

    def tostring(self, xmlroot):
        return self.etree.tostring(xmlroot)

    def Element(self, tag, nsmap):
        return self.etree.Element(tag, nsmap=nsmap)

    def SubElement(self, parent, tag):
        return self.etree.SubElement(parent, tag)

# global ODF Namespaces with LibreOffice prefixes
# LibONS = LibreOfficeNameSpace
LibONS = _XMLNamespaces(LibreOfficeNSMAP, etree)