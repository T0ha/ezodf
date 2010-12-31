#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: filemanager module
# Created: 31.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import os
import zipfile
import tempfile

from datetime import datetime
from collections import OrderedDict

from .manifest import Manifest

class MimeType:
    def __init__(self, mimetype):
        self.mimetype = mimetype
    def tobytes(self):
        return self.mimetype.encode('UTF-8')

class FileObject:
    __slots__ = ['element', 'media_type', 'zipinfo']

    def __init__(self, name, element, media_type=""):
        self.element = element
        self.media_type = media_type
        now = datetime.now().timetuple()
        self.zipinfo = zipfile.ZipInfo(name, now[:6])
        if name != 'mimetype': # ensure 'mimetype' is not compressed
            self.zipinfo.compress_type = zipfile.ZIP_DEFLATED

    @property
    def filename(self):
        return self.zipinfo.filename

class FileManager:
    __slots__ = ['directory', 'manifest', 'zipname']

    def __init__(self, zipname=None):
        self.directory = OrderedDict()
        self.zipname = zipname
        self.manifest = Manifest(self.get_text('META-INF/manifest.xml'))

        # dummy entry to reserve the first entry for 'mimetype'
        # 'mimetype' SHOULD be the first entry in the zipfile and uncompressed
        self.register('mimetype', MimeType('dummy'))
        self.register('META-INF/manifest.xml', self.manifest, 'text/xml')

    def has_zip(self):
        if self.zipname is not None:
            return zipfile.is_zipfile(self.zipname)
        return False

    def tmpfilename(self, filename=None):
        folder = "" if filename is None else os.path.dirname(filename)
        return tempfile.mkstemp('tmp', dir=folder)

    def register(self, name, element, media_type=""):
        self.directory[name] = FileObject(name, element, media_type)
        self.manifest.add(name, media_type)

    def save(self, filename):
        if self.directory['mimetype'].element.mimetype == 'dummy':
            raise ValueError('incorrect mimetype: dummy')

        # alwasy create a new zipfile
        tmpfilename = self.tmpfilename(filename)
        zippo = zipfile.ZipFile(tmpfilename, 'w', zipfile.ZIP_DEFLATED)
        self._tozip(zippo)
        zippo.close()

        # existing document becomes the backup file
        if os.path.exists(filename):
            bakfilename = filename+'.bak'
            # remove existing backupfile
            if os.path.exists(bakfilename):
                os.remove(bakfilename)
            os.rename(filename, bakfilename)

        # rename the new created document
        os.rename(tmpfilename, filename)
        self.zipname = filename

    def get_bytes(self, filename):
        """ Returns a byte stream or None. """
        stream = None
        if self.has_zip():
            zippo = zipfile.ZipFile(self.zipname, 'r')
            try:
                stream = zippo.read(filename)
            except KeyError:
                pass
            zippo.close()
        return stream

    def get_text(self, filename, default=None):
        """ Retuns a str or 'default'. """
        stream = self.get_bytes(filename)
        if stream is not None:
            return str(stream, 'utf-8')
        else:
            return default

    def _tozip(self, zippo):
        processed = []
        for file in self.directory.values():
            if file.media_type == 'text/xml':
                stream = file.element.tobytes(xml_declaration=True)
            else:
                stream = file.element.tobytes()
            zippo.writestr(file.zipinfo, stream)
            processed.append(file.filename)

        self._copy_files(zipobj, processed)

    def _copy_files(self, zipobj, ignore):
        """ Copy all files like pictures and settings except the files in 'ignore'.
        """
        def copyfiles(filenames, fromzip, tozip):
            for name in filenames:
                tozip.writestr(name, fromzip.read(name))

        if self.zipname is None:
            return # nothing to copy
        if not os.path.exists(self.zipname):
            return # nothing to copy

        origzip = zipfile.ZipFile(self.zipname)
        try:
            names = (name for name in origzip.namelist() if name not in ignore)
            copyfiles(names, origzip, zipobj)
        finally:
            origzip.close()

