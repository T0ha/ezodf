#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: BaseClass for ODF content objects
# Created: 03.01.2011
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .xmlns import XML

class BaseClass:
    XMLELEMENT = 'BaseClass'

    def __init__(self, parent=None, xmlroot=None):
        if xmlroot is not None:
            self.xmlroot = xmlroot
        else:
            self.xmlroot = XML.etree.Element(XML(self.XMLELEMENT))
            if parent is not None:
                parent.append(self.xmlroot)

    def __iter__(self):
        return ( XML.to_object(element) for element in self.xmlroot.iter() )

XML.register_class(BaseClass)
