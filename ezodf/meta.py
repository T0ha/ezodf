#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: OOo meta.xml
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from xml.etree import ElementTree as etree
from datetime import datetime

from .xmlns import XMLNamespaces
from .const import ODFNS, VERSION, PACKAGENAME

META_ATTRIBS = frozenset(['generator', 'creation-date', 'initial-creator',
                          'editing-cycles', 'editing-duration'])
DC_ATTRIBS = frozenset(['title', 'subject', 'description', 'creator', 'date',
                        'language'])

class Meta:
    def __init__(self, content=None):
        xmlns = XMLNamespaces(etree=etree)
        if content is None:
            # set namespace prefixes to 'office', 'dc' and 'meta' like LibreOffice
            # self.DC_NS, self.META_NS, self.OFFICE_NS: XMLNamespace object to create
            # Clark Notations for XML node names and attribute names
            self.DC_NS = xmlns.register("dc", ODFNS['dc'])
            self.META_NS = xmlns.register("meta", ODFNS['meta'])
            self.OFFICE_NS = xmlns.register("office", ODFNS['office'])
            self.xmlroot = etree.Element(self.OFFICE_NS('document-meta'))
            self.meta = etree.SubElement(self.xmlroot, self.OFFICE_NS('meta'))
            self.setup()
        else:
            self.xmlroot = xmlns.fromstring(content)
            self.DC_NS = xmlns.get(ODFNS['dc'])
            self.META_NS = xmlns.get(ODFNS['meta'])
            self.OFFICE_NS = xmlns.get(ODFNS['office'])
            self.meta = self.xmlroot.find(self.OFFICE_NS('meta'))

    def setup(self):
        self.__setitem__('generator', PACKAGENAME + '-' + VERSION)
        self.__setitem__('creation-date', datetime.now().isoformat())

    def __setitem__(self, key, value):
        if key in META_ATTRIBS:
            clark_notation = self.META_NS(key)
        elif key in DC_ATTRIBS:
            clark_notation = self.DC_NS(key)
        else:
            raise ValueError('Unsupported Attribute: %s' % attrib)
        element = etree.SubElement(self.meta, clark_notation)
        element.text = value


    def __getitem__(self, key):
        if key in META_ATTRIBS:
            clark_notation = self.META_NS(key)
        elif key in DC_ATTRIBS:
            clark_notation = self.DC_NS(key)
        else:
            raise ValueError('Unsupported Attribute: %s' % attrib)

        element = self.meta.find(clark_notation)
        if element is not None:
            return element.text
        else:
            raise KeyError(key)

    def touch(self):
        self.__setitem__('date', datetime.now().isoformat())

    @staticmethod
    def fromzip(zipfile):
        content = str(zipfile.read('meta.xml'), 'utf-8')
        return Meta(content)

    def tostring(self):
        return ElementTree.tostring(self.xmlroot)
