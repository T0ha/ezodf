#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: support module to handle xml namespaces
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

class XMLNamespace:
    def __init__(self, namespaces=None):
        self._clark2prefix = {}
        self._prefix2clark = {}
        if namespaces is not None:
            self.update(namespaces)

    def update(self, namespaces):
        self._clark2prefix.update(namespaces)
        self._prefix2clark.update(
            { value:key for key, value in namespaces.items() } )

    @property
    def nsmap(self):
        return self._clark2prefix

    def prefix2clark(self, pname):
        """ Convert prefix notation to clark notation. """
        prefix, tag = self.split_prefix(pname)
        return "{%s}%s" % (self._prefix2clark[prefix], tag)

    def clark2prefix(self, cname):
        """ Convert clark notation to prefix notation. """
        uri, tag = self.split_clark(cname)
        return "%s:%s" % (self._clark2prefix[uri], tag)

    def split_prefix(self, tag):
        return tag.split(':', 2)

    def split_clark(self, tag):
        uri, local = tag.split('}', 2)
        return (uri[1:], local)

