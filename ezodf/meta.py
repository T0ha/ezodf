#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF meta.xml document management
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from datetime import datetime

from .xmlns import LibONS
from .const import GENERATOR

METADEFS = {
    'xmlns:office': "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    'xmlns:xlink' : "http://www.w3.org/1999/xlink",
    'xmlns:dc' : "http://purl.org/dc/elements/1.1/",
    'xmlns:meta' : "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
    'xmlns:ooo' : "http://openoffice.org/2004/office",
    'xmlns:grddl' : "http://www.w3.org/2003/g/data-view#",
    'grddl:transformation' : "http://docs.oasis-open.org/office/1.2/xslt/odf2rdf.xsl",
}

VALID_TAGS = frozenset(
    ['meta:generator', 'dc:title', 'dc:description', 'dc:subject',
     'meta:initial-creator', 'dc:creator', 'meta:creation-date', 'dc:date',
     'meta:editing-cycles']
)

# Meta Tags with direct access by __setitem__/__getitem__ interface:
# meta:generator :: application or tool that was used to create or last modify
#                  the XML document.
# dc:title :: title of the document
# dc:description :: brief description of the document
# dc:subject :: subject of the document
# meta:initial-creator :: name of the person who created the document initially
# dc:creator :: name of the person who last modified the document
# meta:creation-date :: date and time when the document was created initially
#                       ISO format  YYYY-MM-DDThh:mm:ss
# dc:date :: date and time when the document was last modified (ISO format)
# meta:editing-cycles :: number of editing cycles the document has been through.
#                        The value of this element is incremented every time
#                        the document is saved.

class Meta:
    # using the default namespace prefixes like LibreOffice: 'office', 'dc'
    # and 'meta'
    generator = GENERATOR # used for meta:generator meta data

    def __init__(self, content=None):
        if content is None:
            self.xmlroot = LibONS.etree.Element(LibONS('office:document-meta'))
            self.meta = LibONS.etree.SubElement(self.xmlroot, LibONS('office:meta'))
            self.setup()
        else:
            # test if content is a string containing the XML data
            if isinstance(content, bytes):
                self.xmlroot = LibONS.etree.fromstring(content)
            # test if content is an ElementTree like node and the node is the
            # root element of the meta document, tag name has to be in clark
            # notation! '{METANAMESPACE}document-meta'
            # raises AttribError if content has no .tag attribute
            elif content.tag == LibONS('office:document-meta'):
                self.xmlroot = content
            else:
                raise ValueError("Unexpected root node: %s" % content.tag)
            self.meta = self.xmlroot.find(LibONS('office:meta'))

    def _set_xmlroot_attribs(self):
        for key, item in METADEFS.items():
            self.xmlroot.set(key, item)

    def setup(self):
        self.__setitem__('meta:creation-date', datetime.now().isoformat())
        self.touch()

    def __setitem__(self, key, value):
        if key not in VALID_TAGS:
            raise KeyError(key)
        cnkey = LibONS(key) # key in clark notation
        element = self.meta.find(cnkey)
        if element is None:
            element = LibONS.etree.SubElement(self.meta, cnkey)
        element.text = value

    def __getitem__(self, key):
        if key not in VALID_TAGS:
            raise KeyError(key)
        element = self.meta.find(LibONS(key))
        if element is not None:
            return element.text
        else:
            raise KeyError(key)

    def touch(self):
        self.__setitem__('dc:date', datetime.now().isoformat())
        self.__setitem__('meta:generator', Meta.generator)

    def inc_editing_cycles(self):
        try:
            count = self.__getitem__('meta:editing-cycles')
            try:
                count = int(count)
                count += 1
            except ValueError:
                count = 1
        except KeyError:
            count = 1
        self.__setitem__('meta:editing-cycles', str(count))

    @staticmethod
    def fromzip(zipfile):
        content = zipfile.read('meta.xml')
        return Meta(content)

    def tostring(self):
        #self._set_xmlroot_attribs()
        return LibONS.tostring(self.xmlroot)

    def keywords(self):
        """ Iterate over all keywords. """
        for keyword in self.meta.findall(LibONS('meta:keyword')):
            yield keyword.text

    def has_keyword(self, keyword):
        """ True if 'keyword' exists, else False. """
        return self._find_keyword(keyword) is not None

    def add_keyword(self, keyword):
        """ Add 'keyword' to meta data. """
        tag = self._find_keyword(keyword)
        if tag is None:
            tag = LibONS.etree.SubElement(LibONS('meta:keyword'))
            tag.text = keyword

    def remove_keyword(self, keyword):
        """ Remove 'keyword' from meta data. """
        tag = self._find_keyword(keyword)
        if tag is not None:
            self.meta.remove(tag)

    def _find_keyword(self, keyword):
        for tag in self.meta.findall(LibONS('meta:keyword')):
            if  keyword == tag.text:
                return tag
        return None

    def usertags(self):
        """ Iterate over all user-defined metatags.

        :returns: (name, value)
        """
        for metatag in self.meta.findall(LibONS('meta:user-defined')):
            yield (metatag.get(LibONS('meta:name')), metatag.text)

    def add_usertag(self, name, value, value_type=None):
        """ Add user-defined metatag. Replaces existing user tags.
        """
        tag = self._find_usertag(name)
        if tag is None:
            tag = LibONS.etree.SubElement(self.meta, LibONS('meta:user-defined'))
            tag.set(LibONS('meta:name'), name)
        tag.text = str(value)
        if value_type is not None:
            tag.set(LibONS('meta:value-type'), value_type)

    def get_usertag(self, name):
        """ Get value of user-defined metatag 'name'.

        Raises KeyError, if 'name' not exist.
        """
        tag = self._find_usertag(name)
        if tag is not None:
            return tag.text
        raise KeyError(name)

    def remove_usertag(self, name):
        """ Remove user defined metatag 'name'.

        Raises KeyError, if 'name' not exist.
        """
        tag = self._find_usertag(name)
        if tag is not None:
            self.meta.remove(tag)
        else:
            raise KeyError(name)

    def _find_usertag(self, name):
        for tag in self.meta.findall(LibONS('meta:user-defined')):
            if name == tag.get(LibONS('meta:name')):
                return tag
        return None
