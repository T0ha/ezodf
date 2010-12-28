#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF Document class
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import os
import zipfile
import tempfile

from .manifest import Manifest
from .meta import Meta
from .styles import Styles
from .content import Content

def open(filename):
    def get_mimetype(zipobj):
        return str(zipobj.read('mimetype'), 'utf-8').strip()

    if zipfile.is_zipfile(filename):
        zipobj = zipfile(filename, mode='r')
        doc = Document(mimetype=get_mimetype(zipobj), filename=filename)
        doc.origfilename = filename
        doc.fromzip(zipobj)
        zipobj.close()
        return doc
    else:
        raise IOError('File does not exist or it is not an ODF file: %s' % filename)

class Document:
    """ OpenDocumentFormat BaseClass """
    def __init__(self, mimetype, filename=None):
        self.filename = filename
        self.origfilename = None # filename of existing document
        self.mimetype = mimetype
        self.manifest = None # META-INF/manifest.xml
        self.content = None
        self.styles = None
        self.meta = None
        self._processed = None # list to store filenames of processed files
        # Setup Document with .setup() or .fromzip()

    def setup(self):
        """ Setup new Document from scratch. """
        self.manifest = Manifest()
        self.meta = Meta()
        self.manifest.add('meta.xml', 'text/xml')

    def fromzip(self, zipobj):
        """ Setup with content from zipfile 'zipobj'. """
        self.manifest = Manifest.fromzip(zipobj)
        self.meta = Meta.fromzip(zipobj)

    def save(self):
        if self.filename is None:
            raise ValueError('No filename specified!')

        folder = os.path.dirname(self.filename)
        tmpfilename = tempfile.mkstemp('tmp', dir=folder)
        zipobj = zipfile.ZipFile(tmpfilename, 'w', zipfile.ZIP_DEFLATED)
        self.tozip(zipobj)
        zipobj.close()
        if os.path.exists(self.filename):
            bakfilename = self.filename+'.bak'
            if os.path.exists(bakfilename):
                os.remove(bakfilename)
            os.rename(self.filename, bakfilename)

        os.rename(tmpfilename, self.filename)

        # preserve filename for the case of saveas(newfilename)
        # because on save() some data has to be copied from the old file to
        # the new file like pictures and settings.
        self.origfilename = self.filename

    def saveas(self, filename):
        self.filename = filename
        self.save()

    def tozip(self, zipobj):
        self._processed = ['mimetype']
        zipobj.writestr('mimetype', self.mimetype.encode('utf-8'))
        self._write_xml(zipobj, 'META-INF/manifest.xml', self.manifest)
        self.meta.touch() # set modification date to now
        self._write_xml(zipobj, 'meta.xml', self.meta)
        self._write_xml(zipobj, 'styles.xml', self.styles)
        self._write_xml(zipobj, 'content.xml', self.content)
        self._write_new_pictures(zipobj)
        self._copy_files(zipobj)
        self._processed = None

    def _write_xml(self, zipobj, filename, xmlobj):
        content = '<?xml version="1.0" encoding="UTF-8"?>' + xmlobj.tostring()
        zipobj.writestr(filename, content.encode('utf-8'))
        self._processed.append(filename)

    def _write_new_pictures(self, zipobj):
        pass

    def _copy_files(self, zipobj):
        """ Copy all unprocessed files like pictures and settings. """
        def copyfiles(filenames, fromzip, tozip):
            for name in filenames:
                tozip.writestr(name, fromzip.read(name))

        if self.origfilename is not None:
            origzip = zipfile.ZipFile(self.origfilename)
            try:
                names = (name for name in origzip.namelist() if name not in self._processed)
                copyfiles(names, origzip, zipobj)
            finally:
                origzip.close()
