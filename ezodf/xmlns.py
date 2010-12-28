#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: support module to handle xml namespaces
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from io import StringIO

class XMLNamespace:
    slots = ['_uri', '_prefix']

    def __init__(self, prefix, uri):
        self._prefix = prefix
        self._uri = uri

    def __call__(self, tag):
        return self.CN(tag)

    def CN(self, tag):
        """ CN = Clark Notation """
        return "{%s}%s" % (self._uri, tag)

    def prefix(self, tag):
        return "%s:%s" % (self._prefix, tag)

class XMLNamespaces:
    def __init__(self, namespaces=None, etree=None):
        self.uri2prefix = {}
        self.prefix2uri = {}
        self._etree = etree

        if namespaces is not None:
            self.update(namespaces)

    def update(self, namespaces):
        for prefix, uri in namespaces.items():
            self.register(prefix, uri)

    def register(self, prefix, uri):
        self.uri2prefix[uri] = prefix
        self.prefix2uri[prefix] = uri
        self._register_at_module(prefix, uri)
        return XMLNamespace(prefix, uri)

    def _register_at_module(self, prefix, uri):
        if self._etree is not None:
            try:
                self._etree._namespace_map[uri] = prefix
            except AttributeError:
                self._etree.register_namespace(prefix, uri)

    def parse(self, source):
        """ Parses an XML section into an element tree. 'source' is a filename
        or file object containing XML data, and it also collects the namespaces
        defined by xmlns attributes. Prefixes treated as global valid
        prefixes, so local redefined prefixes override previouse defined
        prefixes. This is not a valid implementation of XML prefix treatment,
        but to respect local redefined prefixes it would be necessary to
        store the actual valid namespaces for every node, this is to much
        efford and I think all prefixes used in ODF have always the same
        namespace assigned.

        :returns: root XML object created by the etree.Element() factory.
        """
        def parse_nsmap(source):
            events = "start", "start-ns"
            root = None
            ns_map = {}
            for event, elem in self._etree.iterparse(source, events):
                if event == "start-ns":
                    ns_map[elem[0]] = str(elem[1], 'utf-8')
                elif event == "start":
                    if root is None:
                        root = elem
            return root, ns_map

        if self._etree is not None:
            xmlroot, ns_map = parse_nsmap(source)
            self.update(ns_map)
            return xmlroot
        else:
            raise ValueError("ElementTree module not defined!")

    def fromstring(self, text):
        """ Parses an XML section from a string constant. text is a string
        containing XML data. Returns an Element instance. """
        return self.parse(StringIO(text))

    def get(self, prefix_or_uri):
        try:
            uri = self.prefix2uri[prefix_or_uri]
            prefix = prefix_or_uri
        except KeyError:
            prefix = self.uri2prefix[prefix_or_uri]
            uri = prefix_or_uri
        return XMLNamespace(prefix, uri)

    def prefix2clark(self, pname):
        """ Convert prefix notation to clark notation. """
        prefix, tag = self.split_prefix(pname)
        return "{%s}%s" % (self.prefix2uri[prefix], tag)

    def clark2prefix(self, cname):
        """ Convert clark notation to prefix notation. """
        uri, tag = self.split_clark(cname)
        return "%s:%s" % (self.uri2prefix[uri], tag)

    def split_prefix(self, tag):
        if tag.count(':') == 1:
            return tag.split(':')
        else:
            raise ValueError("prefix-notation required 'prefix:local': %s" % tag)

    def split_clark(self, tag):
        if tag[0] == '{':
            uri, local = tag.split('}')
            return (uri[1:], local)
        else:
            raise ValueError("clark-notation required '{uri}local': %s" % tag)
