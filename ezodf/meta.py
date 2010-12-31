#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: ODF meta.xml document management
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

from datetime import datetime

from .xmlns import XML
from .const import META_NSMAP, GENERATOR

TAGS = {
    'generator': 'meta:generator',
    'title': 'dc:title',
    'description': 'dc:description',
    'subject': 'dc:subject',
    'initial-creator': 'meta:initial-creator',
    'creator': 'dc:creator',
    'creation-date': 'meta:creation-date',
    'date': 'dc:date',
    'editing-cycles': 'meta:editing-cycles',
}

# Set/Get Meta Tags by __setitem__/__getitem__ interface:
# -------------------------------------------------------
# generator :: application or tool that was used to create or last modify
#              the XML document.
#
# title :: title of the document
#
# description :: brief description of the document
#
# subject :: subject of the document
#
# initial-creator :: name of the person who created the document initially
#
# creator :: name of the person who last modified the document
#
# creation-date :: date and time when the document was created initially
#                  ISO format  YYYY-MM-DDThh:mm:ss
#
# date :: date and time when the document was last modified (ISO format)
#
# editing-cycles :: number of editing cycles the document has been through.
#                   The value of this element is incremented every time
#                   the document is saved.

class Meta:
    generator = GENERATOR

    def __init__(self, content=None):
        if content is None:
            self.xmlroot = XML.etree.Element(XML('office:document-meta'), nsmap=META_NSMAP)
        else:
            if isinstance(content, bytes):
                self.xmlroot = XML.etree.fromstring(content)
            elif content.tag == XML('office:document-meta'):
                self.xmlroot = content
            else:
                raise ValueError("Unexpected root node: %s" % content.tag)

        self._setup()
        self.keywords = Keywords(self.meta)
        self.usertags = Usertags(self.meta)

    def _setup(self):
        self.meta = self.xmlroot.find(XML('office:meta'))
        if self.meta is None: # this is a new document
            self.meta = XML.etree.SubElement(self.xmlroot, XML('office:meta'))
            self.xmlroot.set(XML('grddl:transformation'), "http://docs.oasis-open.org/office/1.2/xslt/odf2rdf.xsl")
            self['creation-date'] = datetime.now().isoformat()
            self.touch()

    def touch(self):
        self['date'] = datetime.now().isoformat()
        self['generator'] = Meta.generator

    def __setitem__(self, key, value):
        cnkey = XML(TAGS[key]) # key in clark notation
        element = self.meta.find(cnkey)
        if element is None:
            element = XML.etree.SubElement(self.meta, cnkey)
        element.text = value

    def __getitem__(self, key):
        element = self.meta.find(XML(TAGS[key]))
        if element is not None:
            return element.text
        else:
            raise KeyError(key)

    def inc_editing_cycles(self):
        try:
            count = self['editing-cycles']
            try:
                count = int(count) + 1
            except ValueError:
                count = 1
        except KeyError:
            count = 1
        self['editing-cycles'] = str(count)

    def tobytes(self, xml_declaration=None, pretty_print=False):
        """ Returns the XML representation as bytes in 'UTF-8' encoding.

        :param bool xml_declaration: create XML declaration
        :param bool pretty-print: enables formatted XML
        """
        return XML.etree.tostring(self.xmlroot, encoding='UTF-8',
                                  xml_declaration=xml_declaration,
                                  pretty_print=pretty_print)

class Keywords:
    def __init__(self, meta):
        self.meta = meta

    def __iter__(self):
        """ Iterate over all keywords. """
        for keyword in self.meta.findall(XML('meta:keyword')):
            yield keyword.text

    def __contains__(self, keyword):
        """ True if 'keyword' exists, else False. """
        return self._find(keyword) is not None

    def add(self, keyword):
        """ Add 'keyword' to meta data. """
        tag = self._find(keyword)
        if tag is None:
            tag = XML.etree.SubElement(self.meta, XML('meta:keyword'))
            tag.text = keyword

    def remove(self, keyword):
        """ Remove 'keyword' from meta data. """
        tag = self._find(keyword)
        if tag is not None:
            self.meta.remove(tag)

    def _find(self, keyword):
        for tag in self.meta.findall(XML('meta:keyword')):
            if  keyword == tag.text:
                return tag
        return None

class Usertags:
    def __init__(self, meta):
        self.meta = meta

    def __iter__(self):
        """ Iterate over all user-defined metatags.

        :returns: (name, value)
        """
        for metatag in self.meta.findall(XML('meta:user-defined')):
            yield (metatag.get(XML('meta:name')), metatag.text)

    def __contains__(self, name):
        return self._find(name) is not None

    def set(self, name, value, value_type=None):
        """ Set/Replace user-defined metatag.
        """
        tag = self._find(name)
        if tag is None:
            tag = XML.etree.SubElement(self.meta, XML('meta:user-defined'))
            tag.set(XML('meta:name'), name)
        tag.text = str(value)
        if value_type is not None:
            tag.set(XML('meta:value-type'), value_type)

    def __setitem__(self, name, value):
        self.set(name, value)

    def __getitem__(self, name):
        """ Get value of user-defined metatag 'name'.

        Raises KeyError, if 'name' not exist.
        """
        tag = self._find(name)
        if tag is not None:
            return tag.text
        raise KeyError(name)

    def __delitem__(self, name):
        """ Remove user defined metatag 'name'.

        Raises KeyError, if 'name' not exist.
        """
        tag = self._find(name)
        if tag is not None:
            self.meta.remove(tag)
        else:
            raise KeyError(name)

    def typeof(self, key):
        tag = self._find(key)
        if tag is not None:
            return tag.get(XML('meta:value-type'), 'string')
        raise KeyError(key)

    def _find(self, name):
        for tag in self.meta.findall(XML('meta:user-defined')):
            if name == tag.get(XML('meta:name')):
                return tag
        return None
