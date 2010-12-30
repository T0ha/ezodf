#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF content.xml document management
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .const import MIMETYPE_NSMAP
from .xmlns import XML

class Content:
    def __init__(self, mimetype, content=None):
        if content is None:
            self.xmlroot = XML.etree.Element(XML('office:document-content'),
                                             nsmap=MIMETYPE_NSMAP[mimetype])
            self.automatic_styles = XML.etree.SubElement(self.xmlroot,
                                                         XML('office:automatic-styles'))
            self.body = XML.etree.SubElement(self.xmlroot, XML('office:body'))
            self.setup(mimetype)
        else:
            if isinstance(content, bytes):
                self.xmlroot = XML.etree.fromstring(content)
            elif content.tag == XML('office:document-content'):
                self.xmlroot = content
            else:
                raise ValueError("Unexpected root node: %s" % content.tag)
            self.automatic_styles = self.xmlroot.find(XML('office:automatic-styles'))
            self.body = self.xmlroot.find(XML('office:body'))

    def setup(self, mimetype):
        self.xmlroot.set(XML('grddl:transformation'),
                         "http://docs.oasis-open.org/office/1.2/xslt/odf2rdf.xsl")

    @staticmethod
    def fromzip(mimetype, zipfile):
        return Content(mimetype, zipfile.read('content.xml'))
