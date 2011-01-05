#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: BaseClass for ODF content objects
# Created: 03.01.2011
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .xmlns import XML

class BaseClass:
    TAG = 'BaseClass'

    def __init__(self, xmlroot=None):
        if xmlroot is not None:
            self.xmlroot = xmlroot
        else:
            self.xmlroot = XML.etree.Element(self.TAG)

    def __iter__(self):
        return ( XML.to_object(element) for element in self.xmlroot.iter() )

    def __len__(self):
        """ Get count of children """
        return len(self.xmlroot)

    ## index operations

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, element):
        self.insert(index, element)

    def __delitem__(self, index):
        assert isinstance(index, int)
        del self.xmlroot[index]

    def index(self, child):
        """ Get numeric index of `child`. """
        assert isinstance(child, BaseClass)
        return self.xmlroot.index(child.xmlroot)

    def insert(self, index, child):
        """ Insert child at position `index`. """
        assert isinstance(index, int)
        assert isinstance(child, BaseClass)
        self.xmlroot.insert(index, child.xmlroot)
        return child # pass through

    def get(self, index):
        """ Get children at `index` as wrapped object. """
        assert isinstance(index, int)
        xmlelement = self.xmlroot[index]
        return XML.to_object(xmlelement)

    ## list operations

    def add(self, child, insertbefore=None):
        """ Add `child` as to node. """
        if insertbefore is not None:
            position = self.index(insertbefore)
            self.insert(position, child)
        else:
            assert isinstance(child, BaseClass)
            self.xmlroot.append(child.xmlroot)
        return child # pass through

    def remove(self, child):
        """ Remove `child` object from node. """
        assert isinstance(child, BaseClass)
        self.xmlroot.remove(child.xmlroot)

    def clear(self):
        """ Remove all content from node. """
        self.xmlroot.clear()

XML.register_class(BaseClass)
