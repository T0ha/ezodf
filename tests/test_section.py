#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test section
# Created: 17.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# trusted or separately tested modules
from ezodf.xmlns import etree, CN

# objects to test
from ezodf.text import Section

class TestSection(unittest.TestCase):
    def test_init(self):
        s = Section()
        self.assertIsNotNone(s)

    def test_name(self):
        s = Section()
        s.name = 'test'
        self.assertEqual(s.name, 'test')

    def test_unset_protected(self):
        s = Section()
        self.assertFalse(s.protected)

    def test_set_protected_true(self):
        s = Section()
        s.protected = True
        self.assertTrue(s.protected)
        key = s.get_attr(CN('text:protection-key'))
        self.assertTrue(len(key) > 8)

if __name__=='__main__':
    unittest.main()