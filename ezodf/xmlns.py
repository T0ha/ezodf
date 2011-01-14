#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: support module to handle xml namespaces
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from lxml import etree

from .const import ALL_NSMAP

class _XMLNamespaces:
    def __init__(self, namespaces):
        self.prefix2uri = {}
        self.uri2prefix = {}
        self._cache = {}
        self.update(namespaces)

    def update(self, namespaces):
        for prefix, uri in namespaces.items():
            self.register_namespace(prefix, uri)

    def register_namespace(self, prefix, uri):
        self.prefix2uri[prefix] = uri
        self.uri2prefix[uri] = prefix
        self._cache.clear()

    def _prefix2clark_cached(self, tag):
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

class XMLMixin:
    def tobytes(self, xml_declaration=None, pretty_print=False):
        """ Returns the XML representation as bytes in 'UTF-8' encoding.

        :param bool xml_declaration: create XML declaration
        :param bool pretty-print: enables formatted XML
        """
        return etree.tostring(self.xmlnode, encoding='UTF-8',
                              xml_declaration=xml_declaration,
                              pretty_print=pretty_print)

# global ODF Namespaces with OASIS prefixes
XML = _XMLNamespaces(ALL_NSMAP)

def subelement(parent, tag, new=True):
    """ Find/create SubElement `tag` in parent node.
    """
    element = parent.find(tag)
    if (element is None) and (new is True):
        element = etree.SubElement(parent, tag)
    return element

def CN(tag):
    """ Convert `tag` string into clark notation. """
    return XML._prefix2clark_cached(tag)

# tag to class mapper
classmap = {}

def register_class(cls):
    """ Function/Decorator for class registration. """
    classmap[cls.TAG] = cls
    return cls

def wrap(element, default='GenericWrapper'):
    """ Wrap element into a Python wrapper object. """
    try:
        cls = classmap[element.tag]
    except KeyError: # wrap it into the GenericWrapper
        cls = classmap[default]
    return cls(xmlnode=element)
