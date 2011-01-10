#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF Document class
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import zipfile

from .const import MIMETYPES, MIMETYPE_BODYTAG_MAP
from .xmlns import subelement, CN, etree, wrap
from .filemanager import FileManager
from .meta import OfficeDocumentMeta
from .styles import OfficeDocumentStyles
from .content import OfficeDocumentContent
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
            xmlnode = etree.parse(filename)
            return FlatXMLDocument(filename=filename, xmlnode=xmlnode)
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
    """ OpenDocumentFormat Base Class

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

        self.body = self.content.get_application_body(self.application_body_tag)

    @property
    def application_body_tag(self):
        return CN(MIMETYPE_BODYTAG_MAP[self.mimetype])

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
        self.docname = filename

class OTT(ODT):
    """ Open Document Text Template """
    FIXEDMIMETYPE = MIMETYPES['ott']

class ODS(ODT):
    """ Open Document Spreadsheet """
    FIXEDMIMETYPE = MIMETYPES['ods']

class OTS(ODS):
    """ Open Document Spreadsheet Template """
    FIXEDMIMETYPE = MIMETYPES['ots']

class ODP(ODT):
    """ Open Document Presentation """
    FIXEDMIMETYPE = MIMETYPES['odp']

class OTP(ODP):
    """ Open Document Presentation Template """
    FIXEDMIMETYPE = MIMETYPES['otp']

class ODG(ODP):
    """ Open Document Graphic (Drawing) """
    FIXEDMIMETYPE = MIMETYPES['odg']

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
