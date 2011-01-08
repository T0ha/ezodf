#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: filemanager module
# Created: 31.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import os
import zipfile
import random
from datetime import datetime

from .xmlns import etree, CN
from .manifest import Manifest

FNCHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

class FileObject:
    __slots__ = ['element', 'media_type', 'zipinfo']

    def __init__(self, name, element, media_type=""):
        self.element = element
        self.media_type = media_type
        now = datetime.now().timetuple()
        self.zipinfo = zipfile.ZipInfo(name, now[:6])
        self.zipinfo.compress_type = zipfile.ZIP_DEFLATED

    def tobytes(self):
        if hasattr(self.element, 'tobytes'):
            if self.media_type == 'text/xml':
                return self.element.tobytes(xml_declaration=True)
            else:
                return self.element.tobytes()
        else:
            if isinstance(self.element, str):
                return self.element.encode('utf-8')
            elif isinstance(self.element, bytes):
                return self.element
            else:
                raise TypeError('Unsupported type: %s' % type(self.element))

    @property
    def filename(self):
        return self.zipinfo.filename

class FileManager:
    __slots__ = ['directory', 'manifest', 'zipname']

    def __init__(self, zipname=None):
        self.directory = dict()
        self.zipname = zipname
        self.manifest = Manifest(self.get_bytes('META-INF/manifest.xml'))
        self.register('META-INF/manifest.xml', self.manifest, 'text/xml')

    def has_zip(self):
        if self.zipname is not None:
            return zipfile.is_zipfile(self.zipname)
        return False

    def tmpfilename(self, basefile=None):
        def randomname(count):
            return ''.join(random.sample(FNCHARS, count))

        folder = "" if basefile is None else os.path.dirname(basefile)
        while True:
            filename = os.path.abspath(os.path.join(folder, randomname(8)+'.tmp'))
            if not os.path.exists(filename):
                return filename

    def register(self, name, element, media_type=""):
        self.directory[name] = FileObject(name, element, media_type)
        # 'mimetype' need not to be in the manifest.xml file, but it seems
        # not to break the vadility of the manifest file:
        # if name != 'mimetype:
        #     self.manifest.add(name, media_type)
        self.manifest.add(name, media_type)

    def save(self, filename, backup=True):
        # always create a new zipfile
        tmpfilename = self.tmpfilename(filename)
        zippo = zipfile.ZipFile(tmpfilename, 'w', zipfile.ZIP_DEFLATED)
        self._tozip(zippo)
        zippo.close()

        if os.path.exists(filename):
            if backup:
                # existing document becomes the backup file
                bakfilename = filename+'.bak'
                # remove existing backupfile
                if os.path.exists(bakfilename):
                    os.remove(bakfilename)
                os.rename(filename, bakfilename)
            else:
                # just remove the existing document
                os.remove(filename)

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

    def get_xml_element(self, filename):
        content = self.get_bytes(filename)
        if content:
            return etree.XML(content)
        else:
            return None

    def _tozip(self, zippo):
        # write mimetype as first file
        mimetype = self.directory.pop('mimetype')
        # mimetype file should be uncompressed
        mimetype.zipinfo.compress_type = zipfile.ZIP_STORED
        zippo.writestr(mimetype.zipinfo, mimetype.tobytes())
        # mimetype done.
        processed = [mimetype.filename]

        for file in self.directory.values():
            zippo.writestr(file.zipinfo, file.tobytes())
            processed.append(file.filename)

        # push mimetype back to directory
        self.directory['mimetype'] = mimetype
        self._copy_zip_to(zippo, processed)

    def _copy_zip_to(self, newzip, ignore=[]):
        """ Copy all files like pictures and settings except the files in 'ignore'.
        """
        def copyzip(fromzip, tozip):
            for zipinfo in fromzip.filelist:
                if zipinfo.filename not in ignore:
                    tozip.writestr(zipinfo, fromzip.read(zipinfo.filename))

        if self.zipname is None:
            return # nothing to copy
        if not os.path.exists(self.zipname):
            return # nothing to copy

        origzip = zipfile.ZipFile(self.zipname)
        try:
            copyzip(origzip, newzip)
        finally:
            origzip.close()

def check_zipfile_for_oasis_validity(filename, mimetype):
    """ Checks the zipfile structure and least necessary content, but not the
    XML validity of the document.
    """
    def check_manifest(stream):
        xmltree = etree.XML(stream)
        directory = { e.get(CN('manifest:full-path')):e for e in xmltree.findall(CN('manifest:file-entry')) }
        for name in ('content.xml', 'meta.xml', 'styles.xml', '/'):
            if name not in directory:
                return False
        if str(mimetype, encoding='utf-8') != directory['/'].get(CN('manifest:media-type')):
            return False
        return True

    assert isinstance(mimetype, bytes)
    if not zipfile.is_zipfile(filename):
        return False
    # The first file in an OpenDocumentFormat zipfile should be the uncompressed
    # mimetype file, in a regular zipfile this file starts at byte position 30.
    # see also OASIS OpenDocument Specs. Chapter 17.4
    # LibreOffice ignore this requirement and opens all documents with
    # valid content (META-INF/manifest.xml, content.xml).
    with open(filename, 'rb') as f:
        buffer = f.read(38 + len(mimetype))
    if buffer[30:] != b'mimetype'+mimetype:
        return False
    zf = zipfile.ZipFile(filename)
    names = zf.namelist()
    if 'META-INF/manifest.xml' in names:
        manifest = zf.read('META-INF/manifest.xml')
    else:
        manifest = None
    zf.close()

    if manifest is None:
        return False
    # meta.xml and styles.xml are not required, but I think they should
    for filename in ['content.xml', 'meta.xml', 'styles.xml', 'mimetype']:
        if filename not in names:
            return False
    result = check_manifest(manifest)
    return result
