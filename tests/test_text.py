#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test text objects
# Created: 05.01.2011
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import XML
from ezodf.base import BaseClass

# objects to test
from ezodf.text import Paragraph, Span, Heading, Section, List

class TestSpan(unittest.TestCase):
    def test_bare_init(self):
        span = Span()
        self.assertTrue(isinstance(span, BaseClass))
        self.assertEqual(span.xmlroot.tag, XML('text:span'))

    def test_init_xmlroot(self):
        node = XML.etree.Element(XML('text:span'), test="span")
        span = Span(xmlroot=node)
        self.assertTrue(isinstance(span, BaseClass))
        self.assertEqual(span.xmlroot.tag, XML('text:span'))
        self.assertEqual(span.xmlroot.get('test'), "span")

class TestParagraph(unittest.TestCase):
    def test_bare_init(self):
        p = Paragraph()
        self.assertTrue(isinstance(p, BaseClass))
        self.assertEqual(p.xmlroot.tag, XML('text:p'))

    def test_init_xmlroot(self):
        node = XML.etree.Element(XML('text:p'), test="paragraph")
        p = Paragraph(xmlroot=node)
        self.assertTrue(isinstance(p, BaseClass))
        self.assertEqual(p.xmlroot.tag, XML('text:p'))
        self.assertEqual(p.xmlroot.get('test'), "paragraph")

class TestHeading(unittest.TestCase):
    def test_bare_init(self):
        h = Heading()
        self.assertTrue(isinstance(h, BaseClass))
        self.assertEqual(h.xmlroot.tag, XML('text:h'))

    def test_init_xmlroot(self):
        node = XML.etree.Element(XML('text:h'), test="heading")
        h = Heading(xmlroot=node)
        self.assertTrue(isinstance(h, BaseClass))
        self.assertEqual(h.xmlroot.tag, XML('text:h'))
        self.assertEqual(h.xmlroot.get('test'), "heading")

if __name__=='__main__':
    unittest.main()