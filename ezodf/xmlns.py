#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: support module to handle xml namespaces
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from xml.etree import ElementTree

from .const import LibreOfficeNSMAP

class _XMLNamespaces:
    def __init__(self, namespaces, etree):
        self.prefix2uri = {}
        self.etree = etree
        self._cache = {}
        self.update(namespaces)

    def update(self, namespaces):
        for prefix, uri in namespaces.items():
            self.register(prefix, uri)
        self._cache.clear()

    def register(self, prefix, uri):
        self.prefix2uri[prefix] = uri
        self._register_at_module(prefix, uri)

    def _register_at_module(self, prefix, uri):
        if self.etree is not None:
            try:
                self.etree._namespace_map[uri] = prefix
            except AttributeError:
                self.etree.register_namespace(prefix, uri)

    def __call__(self, tag):
        try:
            return self._cache[tag]
        except KeyError:
            if tag[0] == '{': # tag is already in clark notation
                return tag
            else:
                cn = self.prefix2clark(tag)
                self._cache[tag] = cn
                return cn


    def prefix2clark(self, tag):
        """ Convert prefix notation to clark notation. """
        prefix, local = self.split_prefix(tag)
        return "{%s}%s" % (self.prefix2uri[prefix], local)

    def split_prefix(self, tag):
        if tag.count(':') == 1:
            return tag.split(':')
        else:
            raise ValueError("prefix-notation required 'prefix:local': %s" % tag)

# global ODF Namespaces with LibreOffice prefixes
# LibONS = LibreOfficeNameSpace
LibONS = _XMLNamespaces(LibreOfficeNSMAP, ElementTree)