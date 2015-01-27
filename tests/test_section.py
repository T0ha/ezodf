#!/usr/bin/env python
#coding:utf-8
# Purpose: test section
# Created: 17.01.2011
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
from ezodf.xmlns import CN

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
