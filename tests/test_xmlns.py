#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test xmlns module
# Created: 27.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import unittest

from ezodf.xmlns import XMLNamespace

OOONS = XMLNamespace({
    "http://openoffice.org/2000/office": "office",
    "http://openoffice.org/2000/table": "table",
    "http://openoffice.org/2000/style": "style",
    "http://openoffice.org/2000/text": "text",
    "http://openoffice.org/2000/meta": "meta",
    "http://openoffice.org/2000/script": "script",
    "http://openoffice.org/2000/drawing": "drawing",
    "http://openoffice.org/2000/chart": "chart",
    "http://openoffice.org/2000/number": "number",
    "http://openoffice.org/2000/datastyle": "datastyle",
    "http://openoffice.org/2000/dr3d": "dr3d",
    "http://openoffice.org/2000/form": "form",
    "http://openoffice.org/2000/config": "config",
    "http://www.w3.org/1999/XSL/Format": "fo",
    "http://www.w3.org/1999/xlink": "xlink",
    "http://www.w3.org/2000/svg": "svg",
    "http://www.w3.org/1998/Math/MathML": "math",
})

class TestXMLNamespace(unittest.TestCase):
    def test_split_clark(self):
        clark, tag = OOONS.split_clark("{http://openoffice.org/2000/office}p")
        self.assertEqual(clark, 'http://openoffice.org/2000/office')
        self.assertEqual(tag, 'p')

    def test_split_prefix(self):
        prefix, tag = OOONS.split_prefix("office:p")
        self.assertEqual(prefix, 'office')
        self.assertEqual(tag, 'p')

    def test_prefix2clark(self):
        clark = OOONS.prefix2clark("office:p")
        self.assertEqual(clark, "{http://openoffice.org/2000/office}p")

    def test_clark2prefix(self):
        prefix = OOONS.clark2prefix("{http://openoffice.org/2000/office}p")
        self.assertEqual(prefix, "office:p")

    def test_symmetry1(self):
        prefix = OOONS.clark2prefix("{http://openoffice.org/2000/drawing}p")
        self.assertEqual('drawing:p', prefix)

    def test_symmetry2(self):
        clark = OOONS.prefix2clark("text:p")
        self.assertEqual('{http://openoffice.org/2000/text}p', clark)

if __name__=='__main__':
    unittest.main()