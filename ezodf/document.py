#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: document classes
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import zipfile

from .manifest import Manifest
from .xmlns import XMLNamespace

mimetypes = {
    'odt': "application/vnd.oasis.opendocument.text",
    'ott': "application/vnd.oasis.opendocument.text-template",
    'odg': "application/vnd.oasis.opendocument.graphics",
    'otg': "application/vnd.oasis.opendocument.graphics-template",
    'odp': "application/vnd.oasis.opendocument.presentation",
    'otp': "application/vnd.oasis.opendocument.presentation-template",
    'ods': "application/vnd.oasis.opendocument.spreadsheet",
    'ots': "application/vnd.oasis.opendocument.spreadsheet-template",
    'odc': "application/vnd.oasis.opendocument.chart",
    'otc': "application/vnd.oasis.opendocument.chart-template",
    'odi': "application/vnd.oasis.opendocument.image",
    'oti': "application/vnd.oasis.opendocument.image-template",
    'odf': "application/vnd.oasis.opendocument.formula",
    'otf': "application/vnd.oasis.opendocument.formula-template",
    'odm': "application/vnd.oasis.opendocument.text-master",
    'oth': "application/vnd.oasis.opendocument.text-web",
}

file_ext = { mimetype:ext for ext, mimetype in mimetypes.items() }

OOONS = XMLNamespace({
    "http://openoffice.org/2000/office": "office",
    "http://openoffice.org/2000/table": "table",
    "http://openoffice.org/2000/style": "style",
    "http://openoffice.org/2000/text": "text",
    "http://openoffice.org/2000/meta": "meta",
    "http://openoffice.org/2000/script": "script",
    "http://openoffice.org/2000/drawing": "drawing",
    "http://openoffice.org/2000/chart": "chart",
    "http://openoffice.org/2000/number": "number",
    "http://openoffice.org/2000/datastyle": "datastyle",
    "http://openoffice.org/2000/dr3d": "dr3d",
    "http://openoffice.org/2000/form": "form",
    "http://openoffice.org/2000/config": "config",
    "http://www.w3.org/1999/XSL/Format": "fo",
    "http://www.w3.org/1999/xlink": "xlink",
    "http://www.w3.org/2000/svg": "svg",
    "http://www.w3.org/1998/Math/MathML": "math",
})

def open(filename):
    def get_mimetype(zipobj):
        return str(zipobj.read('mimetype'), 'utf-8').strip()

    def open_zipobj(zipobj):
        mimetype = get_mimetype(zipobj)
        return open_document(zipobj, mimetype)

    def open_document(zipobj, mimetype):
        if mimetype.endswith('opendocument.spreadsheet'):
            return document.ODS(zipobj)
        elif mimetype.endswith('opendocument.text'):
            return document.ODT(zipobj)
        elif mimetype.endswith('opendocument.graphics'):
            return document.ODG(zipobj)
        elif mimetype.endswith('opendocument.presentation'):
            return document.ODP(zipobj)
        else:
            raise ValueError('Unsupported mimetype: {0}'.format(mimetype))

    if hasattr(filename, 'infolist'):
        # if filename contains a ZipFile object pass it through
        return open_zipobj(zipobj=filename)
    else:
        zipobj = zipfile.ZipFile(filename, mode='r')
        document = open_zipobj(zipobj)
        zipobj.close()
        return document

class ODFBase:
    """ OpenDocumentFormat BaseClass"""
    def __init__(self, fromzip=None):
        self.xmlroot = None
        self.manifest = None
        self.filename = None

        if fromzip is None:
            # create a new document
            self.setup()
        else:
            # load the document from zipobj
            self.load(fromzip)

    @property
    def file_ext(self):
        return self.__class__.__name__.lower()

    @property
    def mimetype(self):
        return mimetypes[self.file_ext]

    def setup(self):
        self.manifest = Manifest()

    def load(self, fromzip):
        self.manifest = Manifest.from_zipfile(fromzip)

    def save(self):
        zipobj = zipfile.ZipFile(self.filename, 'w')
        self.savetozipobj(zipobj)
        zipobj.close()

    def saveas(self, filename):
        self.filename = filename
        self.save()

    def savetozipobj(self, zipobj):
        self.write_manifest(zipobj)
        self.write_mimetype(zipobj)
        self.write_meta(zipobj)
        self.write_settings(zipobj)
        self.write_styles(zipobj)
        self.write_content(zipobj)
        self.write_Pictures(zipobj)
        self.copy_unprocessed(zipobj)

class ODS(ODFBase):
    """ OpenDocumentSpreadsheet """
    pass

class ODT(ODFBase):
    """ OpenDocumentText """
    pass

class ODG(ODFBase):
    """ OpenDocumentGraphic """
    pass

class ODP(ODFBase):
    """ OpenDocumentPresentation """
    pass
