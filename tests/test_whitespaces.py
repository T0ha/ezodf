#!/usr/bin/env python
#coding:utf-8
# Purpose: test append text
# Created: 06.01.2011
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
from ezodf.xmlns import CN, etree

# objects to test
from ezodf.whitespaces import Spaces, Tabulator, LineBreak, SoftPageBreak
from ezodf.whitespaces import encode_whitespaces, decode_whitespaces

class TestSpaces(unittest.TestCase):
    def test_get_count(self):
        s = Spaces(count=3)
        self.assertEqual(s.count, 3)

    def test_textlen(self):
        s = Spaces(count=3)
        self.assertEqual(s.textlen, 3)

    def test_plaintext(self):
        s = Spaces(count=3)
        self.assertEqual(s.plaintext(), '   ')
        self.assertEqual(str(s), '   ')

    def test_spaces_from_XML(self):
        s = Spaces(xmlnode=etree.XML('<text:s xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:c="3" />'))
        self.assertEqual(s.count, 3)

class TestTabulator(unittest.TestCase):
    def test_init(self):
        t = Tabulator()
        self.assertEqual(t.TAG, CN('text:tab'))
        self.assertEqual(t.xmlnode.tag, CN('text:tab'))

    def test_init_XML(self):
        t = Tabulator(xmlnode=etree.XML('<text:tab xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"/>'))
        self.assertEqual(t.xmlnode.tag, CN('text:tab'))

    def test_textlen(self):
        t = Tabulator()
        self.assertEqual(t.textlen, 1)

    def test_plaintext(self):
        t = Tabulator()
        self.assertEqual(t.plaintext(), '\t')
        self.assertEqual(str(t), '\t')

class TestLineBreak(unittest.TestCase):
    def test_init(self):
        t = LineBreak()
        self.assertEqual(t.TAG, CN('text:line-break'))
        self.assertEqual(t.xmlnode.tag, CN('text:line-break'))

    def test_init_XML(self):
        t = LineBreak(xmlnode=etree.XML('<text:line-break xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"/>'))
        self.assertEqual(t.xmlnode.tag, CN('text:line-break'))

    def test_textlen(self):
        t = LineBreak()
        self.assertEqual(t.textlen, 1)

    def test_plaintext(self):
        t = LineBreak()
        self.assertEqual(t.plaintext(), '\n')
        self.assertEqual(str(t), '\n')

class TestEncodeDecode(unittest.TestCase):
    def test_add_simple_text(self):
        result = encode_whitespaces("TEXT")
        self.assertEqual(result[0], "TEXT")
        self.assertEqual(decode_whitespaces(result), "TEXT")

    def test_add_text_with_1_spc(self):
        txt = "TEXT TAIL"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], txt)
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_with_2_spc(self):
        txt = "TEXT  TAIL"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT ")
        self.assertEqual(result[1].TAG, CN('text:s'))
        self.assertEqual(result[1].count, 1)
        self.assertEqual(result[2], "TAIL")
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_with_5_spc(self):
        txt = "TEXT     TAIL"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT ")
        self.assertEqual(result[1].TAG, CN('text:s'))
        self.assertEqual(result[1].count, 4)
        self.assertEqual(result[2], "TAIL")
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_ends_with_5_spc(self):
        txt = "TEXT     "
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT ")
        self.assertEqual(result[1].TAG, CN('text:s'))
        self.assertEqual(result[1].count, 4)
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_start_with_5_spc(self):
        txt = "     TEXT"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], " ")
        self.assertEqual(result[1].TAG, CN('text:s'))
        self.assertEqual(result[1].count, 4)
        self.assertEqual(result[2], "TEXT")
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_with_groups(self):
        txt = "TEXT  TAIL1  TAIL2"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT ")
        self.assertEqual(result[2], "TAIL1 ")
        self.assertEqual(result[4], "TAIL2")
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_with_tab(self):
        txt = "TEXT\tTAIL"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT")
        self.assertEqual(result[1].TAG, CN('text:tab'))
        self.assertEqual(result[2], "TAIL")
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_with_tab_2spc(self):
        txt = "TEXT\t  TAIL"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT")
        self.assertEqual(result[1].TAG, CN('text:tab'))
        self.assertEqual(result[2], " ")
        self.assertEqual(result[3].TAG, CN('text:s'))
        self.assertEqual(result[4], "TAIL")
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_2spc_tab(self):
        txt = "TEXT  \tTAIL"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT ")
        self.assertEqual(result[1].TAG, CN('text:s'))
        self.assertEqual(result[2].TAG, CN('text:tab'))
        self.assertEqual(result[3], "TAIL")
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_start_with_spc_tab(self):
        txt = "  \tTEXT"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], " ")
        self.assertEqual(result[1].TAG, CN('text:s'))
        self.assertEqual(result[2].TAG, CN('text:tab'))
        self.assertEqual(result[3], "TEXT")
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_with_brk(self):
        txt = "TEXT\nTAIL"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT")
        self.assertEqual(result[1].TAG, CN('text:line-break'))
        self.assertEqual(result[2], "TAIL")
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_with_brk2(self):
        txt = "TEXT\nTAIL\n"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT")
        self.assertEqual(result[1].TAG, CN('text:line-break'))
        self.assertEqual(result[2], "TAIL")
        self.assertEqual(result[3].TAG, CN('text:line-break'))
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_with_brk_before_spc(self):
        txt = "TEXT\nTAIL\n  "
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT")
        self.assertEqual(result[1].TAG, CN('text:line-break'))
        self.assertEqual(result[2], "TAIL")
        self.assertEqual(result[3].TAG, CN('text:line-break'))
        self.assertEqual(result[4], " ")
        self.assertEqual(result[5].TAG, CN('text:s'))
        self.assertEqual(decode_whitespaces(result), txt)

    def test_add_text_with_brk_after_spc(self):
        txt = "TEXT\nTAIL     \n"
        result = encode_whitespaces(txt)
        self.assertEqual(result[0], "TEXT")
        self.assertEqual(result[1].TAG, CN('text:line-break'))
        self.assertEqual(result[2], "TAIL ")
        self.assertEqual(result[3].TAG, CN('text:s'))
        self.assertEqual(result[3].count, 4)
        self.assertEqual(result[4].TAG, CN('text:line-break'))
        self.assertEqual(decode_whitespaces(result), txt)

class TestSoftPageBreak(unittest.TestCase):
    def test_textlen(self):
        br = SoftPageBreak()
        self.assertEqual(0, br.textlen)

    def test_plaintext(self):
        br = SoftPageBreak()
        self.assertEqual('', br.plaintext())

if __name__=='__main__':
    unittest.main()
