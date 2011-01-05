#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test text objects
# Created: 05.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import etree, CN
from ezodf.base import BaseClass

# objects to test
from ezodf.text import Paragraph, Span, Heading, Section, List

class TestSpan(unittest.TestCase):
    def test_bare_init(self):
        span = Span()
        self.assertTrue(isinstance(span, BaseClass))
        self.assertEqual(span.xmlroot.tag, CN('text:span'))

    def test_init_xmlroot(self):
        node = etree.Element(CN('text:span'), test="span")
        span = Span(xmlroot=node)
        self.assertTrue(isinstance(span, BaseClass))
        self.assertEqual(span.xmlroot.tag, CN('text:span'))
        self.assertEqual(span.xmlroot.get('test'), "span")

DATA1 = '<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"'\
        ' text:style-name="Standard">Lorem ipsum <text:span text:style-name="T1">'\
        'dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor '\
        'invidunt ut labore et dolore <text:s text:c="3"/>magna </text:span>'\
        '<text:span text:style-name="T2">aliquyam</text:span>'\
        '<text:span text:style-name="T1"> erat, sed diam voluptua. '\
        'At vero eos et accusam et justo duo dolores et ea rebum. Stet '\
        'clita kasd</text:span> gubergren, no sea takimata sanctus est '\
        'Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur '\
        'sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore '\
        'et dolore magna aliquyam erat, sed diam voluptua. At vero eos '\
        'et accusam et justo duo dolores et ea rebum. Stet clita kasd '\
        'gubergren, no sea takimata sanctus est Lorem ipsum dolor sit '\
        'amet.</text:p>'

class TestParagraph(unittest.TestCase):
    def test_bare_init(self):
        p = Paragraph()
        self.assertTrue(isinstance(p, BaseClass))
        self.assertEqual(p.xmlroot.tag, CN('text:p'))

    def test_init_xmlroot(self):
        node = etree.Element(CN('text:p'), test="paragraph")
        p = Paragraph(xmlroot=node)
        self.assertTrue(isinstance(p, BaseClass))
        self.assertEqual(p.xmlroot.tag, CN('text:p'))
        self.assertEqual(p.xmlroot.get('test'), "paragraph")

class TestHeading(unittest.TestCase):
    def test_bare_init(self):
        h = Heading()
        self.assertTrue(isinstance(h, BaseClass))
        self.assertEqual(h.xmlroot.tag, CN('text:h'))

    def test_init_xmlroot(self):
        node = etree.Element(CN('text:h'), test="heading")
        h = Heading(xmlroot=node)
        self.assertTrue(isinstance(h, BaseClass))
        self.assertEqual(h.xmlroot.tag, CN('text:h'))
        self.assertEqual(h.xmlroot.get('test'), "heading")

if __name__=='__main__':
    unittest.main()