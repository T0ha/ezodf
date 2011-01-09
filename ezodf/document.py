#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF Document class
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import zipfile

from .const import MIMETYPES
from .xmlns import subelement, CN, etree, pyobj
from .filemanager import FileManager
from .meta import OfficeDocumentMeta
from .styles import OfficeDocumentStyles
from .content import OfficeDocumentContent
from .content import TextBody, SpreadsheetBody, PresentationBody, DrawingBody
from .flatxmlfile import FlatXMLDocument

class InvalidFiletypeError(TypeError):
    pass

def open(filename):
    if zipfile.is_zipfile(filename):
        fm = FileManager(filename)
        mimetype = fm.get_text('mimetype')
        try:
            return DOCUMENTCLASS[mimetype](filemanager=fm)
        except KeyError:
            # just the basics for: chart, image, formula, templates
            return Document(filemanager=fm, mimetype=mimetype)
    else:
        try:
            xmlroot = etree.parse(filename)
            return FlatXMLDocument(filename=filename, xmlroot=xmlroot)
        except etree.ParseError:
            pass
        raise IOError("File '%s' is neither a zip-package nor a flat XML OpenDocumentFormat file." % filename)


def new_from_template(filename, templatename):
    if zipfile.is_zipfile(templatename):
        fm = FileManager(templatename)
        mimetype = fm.get_text('mimetype')
        if mimetype.endswith('-template'):
            mimetype = mimetype[:-9]
        try:
            return DOCUMENTCLASS[mimetype](filename=filename, filemanager=fm)
        except KeyError:
            raise InvalidFiletypeError("Unsupported mimetype: %s".format(mimetype))
    else:
        raise IOError('File does not exist or it is not a zipfile: %s' % templatename)


class Document:
    """ OpenDocumentFormat BaseClass

    The `Document` class can hold every ODF file type.
    """
    def __init__(self, filemanager, mimetype):
        self.filemanager = fm = FileManager() if filemanager is None else filemanager
        self.docname = fm.zipname
        self.backup = True

        # add doctype to manifest
        self.filemanager.manifest.add('/', mimetype)

        self.mimetype = mimetype
        fm.register('mimetype', self.mimetype)

        self.meta = OfficeDocumentMeta(fm.get_xml_element('meta.xml'))
        fm.register('meta.xml', self.meta, 'text/xml')

        self.styles = OfficeDocumentStyles(fm.get_xml_element('styles.xml'))
        fm.register('styles.xml', self.styles, 'text/xml')

        self.content = OfficeDocumentContent(mimetype, fm.get_xml_element('content.xml'))
        fm.register('content.xml', self.content, 'text/xml')

    def save(self):
        if self.docname is None:
            raise IOError('No filename specified!')
        self.meta.touch() # set modification date to now
        self.meta.inc_editing_cycles()
        self.filemanager.save(self.docname, backup=self.backup)

    def saveas(self, filename):
        self.docname = filename
        self.save()

class ODT(Document):
    """ Open Document Text """
    FIXEDMIMETYPE = MIMETYPES['odt']
    def __init__(self, filename=None, filemanager=None):
        super(ODT, self).__init__(filemanager, self.FIXEDMIMETYPE)
        assert self.mimetype == self.FIXEDMIMETYPE
        self.docname = filename
        self.body = TextBody(self.content.xmlroot)
        self.fonts = pyobj(subelement(self.content.xmlroot, CN('office:font-face-decls')))

class OTT(ODT):
    """ Open Document Text Template """
    FIXEDMIMETYPE = MIMETYPES['ott']

class ODS(Document):
    """ Open Document Spreadsheet """
    FIXEDMIMETYPE = MIMETYPES['ods']

    def __init__(self, filename=None, filemanager=None):
        super(ODS, self).__init__(filemanager, self.FIXEDMIMETYPE)
        assert self.mimetype == self.FIXEDMIMETYPE
        self.docname = filename
        self.body = SpreadsheetBody(self.content.xmlroot)
        self.fonts = pyobj(subelement(self.content.xmlroot, CN('office:font-face-decls')))

class OTS(ODS):
    """ Open Document Spreadsheet Template """
    FIXEDMIMETYPE = MIMETYPES['ots']

class ODP(Document):
    """ Open Document Presentation """
    FIXEDMIMETYPE = MIMETYPES['odp']
    def __init__(self, filename=None, filemanager=None):
        super(ODP, self).__init__(filemanager, self.FIXEDMIMETYPE)
        assert self.mimetype == self.FIXEDMIMETYPE
        self.docname = filename
        self.body = PresentationBody(self.content.xmlroot)

class OTP(ODP):
    """ Open Document Presentation Template """
    FIXEDMIMETYPE = MIMETYPES['otp']

class ODG(Document):
    """ Open Document Graphic (Drawing) """
    FIXEDMIMETYPE = MIMETYPES['odg']
    def __init__(self, filename=None, filemanager=None):
        super(ODG, self).__init__(filemanager, self.FIXEDMIMETYPE)
        assert self.mimetype == self.FIXEDMIMETYPE
        self.docname = filename
        self.body = DrawingBody(self.content.xmlroot)

class OTG(ODG):
    """ Open Document Graphic (Drawing) Template """
    FIXEDMIMETYPE = MIMETYPES['otg']

DOCUMENTCLASS = {
    MIMETYPES['odt']: ODT,
    MIMETYPES['ott']: OTT,
    MIMETYPES['ods']: ODS,
    MIMETYPES['ots']: OTS,
    MIMETYPES['odg']: ODG,
    MIMETYPES['otg']: OTG,
    MIMETYPES['odp']: ODP,
    MIMETYPES['otp']: OTP,
}
