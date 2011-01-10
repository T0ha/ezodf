#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF content.xml document management
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from .const import MIMETYPE_NSMAP
from .xmlns import XMLMixin, subelement, CN, etree
from .base import BaseClass

class OfficeDocumentContent(XMLMixin):
    TAG = CN('office:document-content')

    def __init__(self, mimetype, xmlnode=None):

        if xmlnode is None:
            self.xmlnode = etree.Element(self.TAG, nsmap=MIMETYPE_NSMAP[mimetype])
        elif xmlnode.tag == self.TAG:
            self.xmlnode = xmlnode
        else:
            raise ValueError("Unexpected root node: %s" % xmlnode.tag)
        self._setup(mimetype)

    def _setup(self, mimetype):
        # these elements are common to all document types
        # The element office:scripts always exists but is always empty
        # so I dont't keep a reference to it
        subelement(self.xmlnode, CN('office:scripts'))
        self.automatic_styles = subelement(self.xmlnode, CN('office:automatic-styles'))

class _AbstractBody(BaseClass):
    def __init__(self, parent):
        # parent type should be etree.Element
        assert parent.tag == CN('office:document-content')
        # The office:body element is just frame element for the real document content:
        # office:text, office:spreadsheet, office:presentation, office:drawing
        body = subelement(parent, CN('office:body'))
        # set xmlnode here, no need to call constructor of BaseClass
        self.xmlnode = subelement(body, self.TAG)

class TextBody(_AbstractBody):
    TAG = CN('office:text')

class SpreadsheetBody(_AbstractBody):
    TAG = CN('office:spreadsheet')

class PresentationBody(_AbstractBody):
    TAG = CN('office:presentation')

class DrawingBody(_AbstractBody):
    TAG = CN('office:drawing')
