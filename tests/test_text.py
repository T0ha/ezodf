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
from ezodf.text import Paragraph, Span, Heading


SPANDATA = '<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
           'text:style-name="T2">aliquyam</text:span>'

SPANDATA_SPC = '<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
               'text:style-name="T2">aliquyam <text:s text:c="3"/></text:span>'

SPANDATA_BRK = '<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
               'text:style-name="T2">Line1<text:line-break />Line2</text:span>'

SPANDATA_TAB = '<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
               'text:style-name="T2">Line1<text:tab />Line2</text:span>'

SPANDATA_ALL = '<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '\
               'text:style-name="T2">Line1<text:line-break />Line2<text:tab />123 '\
               '<text:s text:c="3"/>tail</text:span>'

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

    def test_init_XML(self):
        node = etree.XML(SPANDATA)
        span = Span(xmlroot=node)
        self.assertTrue(isinstance(span, BaseClass))
        self.assertEqual(span.xmlroot.tag, CN('text:span'))

    def test_textlen(self):
        span = Span(xmlroot=etree.XML(SPANDATA))
        self.assertEqual(span.textlen, 8)

    def test_textlen_with_spaces(self):
        span = Span(xmlroot=etree.XML(SPANDATA_SPC))
        self.assertEqual(span.textlen, 12)

    def test_textlen_with_line_break(self):
        span = Span(xmlroot=etree.XML(SPANDATA_BRK))
        self.assertEqual(span.textlen, 11)

    def test_textlen_with_tab(self):
        span = Span(xmlroot=etree.XML(SPANDATA_TAB))
        self.assertEqual(span.textlen, 11)

    def test_textlen_with_all(self):
        span = Span(xmlroot=etree.XML(SPANDATA_ALL))
        self.assertEqual(span.textlen, 23)

    def test_plaintext(self):
        span = Span(xmlroot=etree.XML(SPANDATA))
        self.assertEqual(span.plaintext(), 'aliquyam')

    def test_plaintext_with_spaces(self):
        span = Span(xmlroot=etree.XML(SPANDATA_SPC))
        self.assertEqual(span.plaintext(), 'aliquyam    ')

    def test_plaintext_with_line_break(self):
        span = Span(xmlroot=etree.XML(SPANDATA_BRK))
        self.assertEqual(span.plaintext(), 'Line1\nLine2')

    def test_plaintext_with_tab(self):
        span = Span(xmlroot=etree.XML(SPANDATA_TAB))
        self.assertEqual(span.plaintext(), 'Line1\tLine2')

    def test_plaintext_with_all(self):
        span = Span(xmlroot=etree.XML(SPANDATA_ALL))
        self.assertEqual(span.plaintext(), 'Line1\nLine2\t123    tail')

    def test_get_style_name(self):
        span = Span(xmlroot=etree.XML(SPANDATA))
        self.assertEqual(span.style_name, 'T2')

    def test_set_style_name(self):
        span = Span(xmlroot=etree.XML(SPANDATA))
        span.style_name = "XXX"
        self.assertEqual(span.style_name, 'XXX')

    def test_append_text(self):
        txt = "TEXT"
        span = Span(text=txt)
        self.assertEqual(span.text, txt)
        self.assertEqual(span.plaintext(), txt)

    def test_append_text_2(self):
        txt = "TEXT  TAIL"
        span = Span(text=txt)
        self.assertEqual(span.text, "TEXT ")
        self.assertEqual(span[0].TAG, CN('text:s'))
        self.assertEqual(span[0].tail, "TAIL")
        self.assertEqual(span.plaintext(), txt)

    def test_append_text_3(self):
        txt = "TEXT  TAIL \n  \t    "
        span = Span(text=txt)
        self.assertEqual(span.text, "TEXT ")
        self.assertEqual(span[0].TAG, CN('text:s'))
        self.assertEqual(span[0].tail, "TAIL ")
        self.assertEqual(span[1].TAG, CN('text:line-break'))
        self.assertEqual(span[1].tail, " ")
        self.assertEqual(span[2].TAG, CN('text:s'))
        self.assertEqual(span[2].tail, None)
        self.assertEqual(span[3].TAG, CN('text:tab'))
        self.assertEqual(span[3].tail, " ")
        self.assertEqual(span[4].TAG, CN('text:s'))
        self.assertEqual(span[4].count, 3)
        self.assertEqual(span.plaintext(), txt)

    def test_append_text_4(self):
        span = Span(text="TEXT")
        span.append_plaintext("  TAIL")
        self.assertEqual(span.text, "TEXT ")
        self.assertEqual(span[0].TAG, CN('text:s'))
        self.assertEqual(span[0].tail, "TAIL")

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