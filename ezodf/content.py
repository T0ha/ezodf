#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF content.xml document management
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .const import MIMETYPE_NSMAP
from .xmlns import XML, XMLMixin, subelement

class Content(XMLMixin):
    def __init__(self, mimetype, content=None):

        if content is None:
            self.xmlroot = XML.etree.Element(XML('office:document-content'),
                                             nsmap=MIMETYPE_NSMAP[mimetype])
            self.xmlroot.set(XML('grddl:transformation'),
                             "http://docs.oasis-open.org/office/1.2/xslt/odf2rdf.xsl")
        else:
            if isinstance(content, bytes):
                self.xmlroot = XML.etree.fromstring(content)
            elif content.tag == XML('office:document-content'):
                self.xmlroot = content
            else:
                raise ValueError("Unexpected root node: %s" % content.tag)

        self.setup(mimetype)

    def setup(self, mimetype):
        # these elements are common to all document types
        # The element office:scripts always exists but is always empty
        # so I dont't keep a reference to it
        subelement(self.xmlroot, XML('office:scripts'))
        self.automatic_styles = subelement(self.xmlroot, XML('office:automatic-styles'))

class _AbstractBody:
    def __init__(self, parent, tag):
        # parent type should be etree.Element
        assert parent.tag == XML('office:document-content')
        # The office:body element is just frame element for the real document content:
        # office:text, office:spreadsheet, office:presentation, office:drawing
        body = subelement(parent, XML('office:body'))
        self.xmlroot = subelement(body, tag)

class TextBody(_AbstractBody):
    def __init__(self, parent):
        super (TextBody, self).__init__(parent, tag=XML('office:text'))

class SpreadsheetBody(_AbstractBody):
    def __init__(self, parent):
        super (SpreadsheetBody, self).__init__(parent, tag=XML('office:spreadsheet'))

class PresentationBody(_AbstractBody):
    def __init__(self, parent):
        super (PresentationBody, self).__init__(parent, tag=XML('office:presentation'))

class DrawingBody(_AbstractBody):
    def __init__(self, parent):
        super (DrawingBody, self).__init__(parent, tag=XML('office:drawing'))
