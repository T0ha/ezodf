#!/usr/bin/env python
#coding:utf-8
# Purpose: test text objects
# Created: 05.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# trusted or separately tested modules
from ezodf.xmlns import etree, CN
from ezodf.base import GenericWrapper

# objects to test
from ezodf.text import Paragraph, Span, Heading, NumberedParagraph, Hyperlink


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
        self.assertTrue(isinstance(span, GenericWrapper))
        self.assertEqual(span.xmlnode.tag, CN('text:span'))

    def test_init_xmlroot(self):
        node = etree.Element(CN('text:span'), test="span")
        span = Span(xmlnode=node)
        self.assertTrue(isinstance(span, GenericWrapper))
        self.assertEqual(span.xmlnode.tag, CN('text:span'))
        self.assertEqual(span.xmlnode.get('test'), "span")

    def test_init_XML(self):
        node = etree.XML(SPANDATA)
        span = Span(xmlnode=node)
        self.assertTrue(isinstance(span, GenericWrapper))
        self.assertEqual(span.xmlnode.tag, CN('text:span'))

    def test_textlen(self):
        span = Span(xmlnode=etree.XML(SPANDATA))
        self.assertEqual(span.textlen, 8)

    def test_textlen_with_spaces(self):
        span = Span(xmlnode=etree.XML(SPANDATA_SPC))
        self.assertEqual(span.textlen, 12)

    def test_textlen_with_line_break(self):
        span = Span(xmlnode=etree.XML(SPANDATA_BRK))
        self.assertEqual(span.textlen, 11)

    def test_textlen_with_tab(self):
        span = Span(xmlnode=etree.XML(SPANDATA_TAB))
        self.assertEqual(span.textlen, 11)

    def test_textlen_with_all(self):
        span = Span(xmlnode=etree.XML(SPANDATA_ALL))
        self.assertEqual(span.textlen, 23)

    def test_plaintext(self):
        span = Span(xmlnode=etree.XML(SPANDATA))
        self.assertEqual(span.plaintext(), 'aliquyam')

    def test_plaintext_with_spaces(self):
        span = Span(xmlnode=etree.XML(SPANDATA_SPC))
        self.assertEqual(span.plaintext(), 'aliquyam    ')

    def test_plaintext_with_line_break(self):
        span = Span(xmlnode=etree.XML(SPANDATA_BRK))
        self.assertEqual(span.plaintext(), 'Line1\nLine2')

    def test_plaintext_with_tab(self):
        span = Span(xmlnode=etree.XML(SPANDATA_TAB))
        self.assertEqual(span.plaintext(), 'Line1\tLine2')

    def test_plaintext_with_all(self):
        span = Span(xmlnode=etree.XML(SPANDATA_ALL))
        self.assertEqual(span.plaintext(), 'Line1\nLine2\t123    tail')

    def test_get_style_name(self):
        span = Span(xmlnode=etree.XML(SPANDATA))
        self.assertEqual(span.style_name, 'T2')

    def test_set_style_name(self):
        span = Span(xmlnode=etree.XML(SPANDATA))
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
        span.append_text("  TAIL")
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
        self.assertTrue(isinstance(p, GenericWrapper))
        self.assertEqual(p.xmlnode.tag, CN('text:p'))

    def test_init_xmlroot(self):
        node = etree.Element(CN('text:p'), test="paragraph")
        p = Paragraph(xmlnode=node)
        self.assertTrue(isinstance(p, GenericWrapper))
        self.assertEqual(p.xmlnode.tag, CN('text:p'))
        self.assertEqual(p.xmlnode.get('test'), "paragraph")

    def test_cond_style_name(self):
        p = Paragraph()
        p.cond_style_name = "CONDSTYLE"
        self.assertEqual(p.cond_style_name, "CONDSTYLE")
        self.assertIsNotNone(p.xmlnode.get(CN('text:cond-style-name')))

    def test_ID(self):
        p = Paragraph()
        p.ID = "ID001"
        self.assertEqual(p.ID, "ID001")
        self.assertIsNotNone(p.xmlnode.get(CN('text:id')))

class TestNumberedParagraph(unittest.TestCase):
    def test_init_1(self):
        np = NumberedParagraph()
        self.assertEqual(np.xmlnode.tag, CN('text:numbered-paragraph'))

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            np = NumberedParagraph('text')

    def test_paragraph_content(self):
        np = NumberedParagraph(Paragraph('text'))
        res = np.content
        self.assertEqual(res.plaintext(), 'text')

    def test_heading_content(self):
        np = NumberedParagraph(Heading('text'))
        res = np.content
        self.assertEqual(res.plaintext(), 'text')

    def test_no_content(self):
        np = NumberedParagraph()
        newp = np.content
        self.assertEqual(newp.kind, 'Paragraph')
        newp.append_text('text')
        self.assertEqual(np.content.plaintext(), 'text')

    def test_level_0(self):
        np = NumberedParagraph()
        np.level = 0
        self.assertEqual(np.level, 1)

    def test_level_1(self):
        np = NumberedParagraph()
        np.level = '1'
        self.assertEqual(np.level, 1)

    def test_level_2(self):
        np = NumberedParagraph()
        np.level = 2.
        self.assertEqual(np.level, 2)

class TestNumberingMixin(unittest.TestCase):
    def test_unset_start_value(self):
        np = NumberedParagraph()
        self.assertIsNone(np.start_value)

    def test_start_value_0(self):
        np = NumberedParagraph()
        np.start_value = 0
        self.assertEqual(np.start_value, 1)

    def test_start_value_1(self):
        np = NumberedParagraph()
        np.start_value = '1'
        self.assertEqual(np.start_value, 1)

    def test_start_value_2(self):
        np = NumberedParagraph()
        np.start_value = 2.
        self.assertEqual(np.start_value, 2)

    def test_unset_formatted_number(self):
        np = NumberedParagraph()
        self.assertIsNone(np.formatted_number)

    def test_formatted_value(self):
        np = NumberedParagraph()
        np.formatted_number = '#2'
        self.assertEqual(np.formatted_number, '#2')


class TestHeading(unittest.TestCase):
    def test_bare_init(self):
        h = Heading()
        self.assertTrue(isinstance(h, GenericWrapper))
        self.assertEqual(h.xmlnode.tag, CN('text:h'))

    def test_init_xmlroot(self):
        node = etree.Element(CN('text:h'), test="heading")
        h = Heading(xmlnode=node)
        self.assertTrue(isinstance(h, GenericWrapper))
        self.assertEqual(h.xmlnode.tag, CN('text:h'))
        self.assertEqual(h.xmlnode.get('test'), "heading")

    def test_outline_level_0(self):
        h = Heading('text', outline_level=0)
        self.assertEqual(h.outline_level, 1)

    def test_outline_level_1(self):
        h = Heading('text')
        self.assertEqual(h.outline_level, 1)

    def test_outline_level_2(self):
        h = Heading('text')
        h.outline_level = 2.
        self.assertEqual(h.outline_level, 2)

    def test_unset_restart_numbering(self):
        h = Heading('text')
        self.assertFalse(h.restart_numbering)

    def test_restart_numbering_true(self):
        h = Heading('text')
        h.restart_numbering = True
        self.assertTrue(h.restart_numbering)

    def test_restart_numbering_true(self):
        h = Heading('text')
        h.restart_numbering = False
        self.assertFalse(h.restart_numbering)

    def test_unset_suppress_numbering(self):
        h = Heading('text')
        self.assertFalse(h.suppress_numbering)

    def test_suppress_numbering_true(self):
        h = Heading('text')
        h.suppress_numbering = True
        self.assertTrue(h.suppress_numbering)

    def test_suppress_numbering_false(self):
        h = Heading('text')
        h.suppress_numbering = False
        self.assertFalse(h.suppress_numbering)

class TestHyperlink(unittest.TestCase):
    def test_init(self):
        h = Hyperlink(xmlnode=None)
        self.assertIsNotNone(h)

    def test_unset_name(self):
        h = Hyperlink(xmlnode=None)
        self.assertIsNone(h.name)

    def test_name(self):
        h = Hyperlink(xmlnode=None)
        h.name = 'test'
        self.assertEqual(h.name, 'test')

    def test_unset_href(self):
        h = Hyperlink(xmlnode=None)
        self.assertIsNone(h.href)

    def test_href(self):
        h = Hyperlink(xmlnode=None)
        h.href = 'http://x.html'
        self.assertEqual(h.href, 'http://x.html')

    def test_target_frame(self):
        h = Hyperlink(xmlnode=None)
        h.target_frame = 'xtarget'
        self.assertEqual(h.target_frame, 'xtarget')
        self.assertEqual(h.get_attr(CN('xlink:show')), 'replace')

    def test_target_frame_blank(self):
        h = Hyperlink(xmlnode=None)
        h.target_frame = '_blank'
        self.assertEqual(h.target_frame, '_blank')
        self.assertEqual(h.get_attr(CN('xlink:show')), 'new')

if __name__=='__main__':
    unittest.main()
