#!/usr/bin/env python
#coding:utf-8
# Purpose: test node organizer
# Created: 31.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

# Standard Library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# test helpers
from mytesttools import create_node

# objects to test
from ezodf.nodeorganizer import EpilogueTagBlock

def getETB(nodes, tags='xyz'):
    return EpilogueTagBlock(create_node(nodes), tags)

class TestEpilogueTagBlockBasics(unittest.TestCase):
    def test_xmlnode_is_none_error(self):
        with self.assertRaises(ValueError):
            EpilogueTagBlock(None, '')

    def test_no_epilogue_tags(self):
        with self.assertRaises(ValueError):
            EpilogueTagBlock(create_node('abc'), '')

    def test_unique_order_tags(self):
        with self.assertRaises(ValueError):
            EpilogueTagBlock(create_node('abc'), 'abcc')

    def test_get_count(self):
        etb = getETB('aabbccghixxyyzz')
        self.assertEqual(len(etb), 6)

    def test_get_epilogue_only_tree(self):
        etb = getETB('xxyyzz')
        self.assertEqual(len(etb), 6)

    def test_get_count_without_eiplogue(self):
        etb = getETB('aabbccghi')

        self.assertEqual(len(etb), 0)

    def test_get_count_empty_tree(self):
        etb = getETB('')
        self.assertEqual(len(etb), 0)

    def test_get_count_from_not_well_formed_tree(self):
        etb = getETB('aabbccgxzhi')
        self.assertEqual(len(etb), 0)

class TestEpilogueTagBlockTagInfo(unittest.TestCase):
    def test_get_tag_info_z(self):
        etb = getETB('aabbccghixxyyzz')
        start_index, count = etb.tag_info('z')
        self.assertEqual((13, 2), (start_index, count))

    def test_get_tag_info_x(self):
        etb = getETB('aabbccghixxxyyzz')
        start_index, count = etb.tag_info('x')
        self.assertEqual((9, 3), (start_index, count))

    def test_get_tag_info_for_not_existing_tag(self):
        etb = getETB('aabbccghixxxzz')
        start_index, count = etb.tag_info('y')
        self.assertEqual((-1, 0), (start_index, count))

    def test_get_tag_info_invalid_tag_error(self):
        etb = getETB('aabbccghixxxzz')
        with self.assertRaises(ValueError):
            etb.tag_info('w')

    def test_get_tag_info_for_tag_not_in_epilogue(self):
        etb = getETB('aabbccghixxxgyyzz')
        start_index, count = etb.tag_info('x')
        self.assertEqual((-1, 0), (start_index, count))

class TestEpilogueTagBlockInsertPositionAfter(unittest.TestCase):

    def test_tag_error(self):
        tb = EpilogueTagBlock(create_node('abc'), 'xyz')
        with self.assertRaises(ValueError):
            tb.insert_position_after('d')

    def test_after_existing_tag(self):
        tb = getETB('aabbccghixxyyzz', 'xyz')

        self.assertEqual(tb.insert_position_after('x'), 11)
        self.assertEqual(tb.insert_position_after('y'), 13)
        self.assertEqual(tb.insert_position_after('z'), 15)

    def test_after_not_existing_tag(self):
        tb = getETB('aabbccghixxzz', 'xyz')

        self.assertEqual(tb.insert_position_after('x'), 11)
        self.assertEqual(tb.insert_position_after('y'), 11)
        self.assertEqual(tb.insert_position_after('z'), 13)

    def test_without_epilogue(self):
        tb = getETB('aabbccghi', 'xyz')

        self.assertEqual(tb.insert_position_after('x'), 9)
        self.assertEqual(tb.insert_position_after('y'), 9)
        self.assertEqual(tb.insert_position_after('y'), 9)

    def test_for_empty_node(self):
        tb = getETB('', 'xyz')

        self.assertEqual(tb.insert_position_after('x'), 0)
        self.assertEqual(tb.insert_position_after('y'), 0)
        self.assertEqual(tb.insert_position_after('z'), 0)

class TestEpilogueTagBlockInsertPositionBefore(unittest.TestCase):
    def test_tag_error(self):
        tb = getETB('abc', 'xyz')

        with self.assertRaises(ValueError):
            tb.insert_position_before('d')

    def test_before_existing_tag(self):
        tb = getETB('aabbccghixxyyzz', 'xyz')

        self.assertEqual(tb.insert_position_before('x'), 9)
        self.assertEqual(tb.insert_position_before('y'), 11)
        self.assertEqual(tb.insert_position_before('z'), 13)

    def test_before_not_existing_tag(self):
        tb = getETB('aabbccghixxzz', 'xyz')

        self.assertEqual(tb.insert_position_before('x'), 9)
        self.assertEqual(tb.insert_position_before('y'), 11)
        self.assertEqual(tb.insert_position_before('z'), 11)

    def test_without_epilogue(self):
        tb = getETB('aabbccghi', 'xyz')

        self.assertEqual(tb.insert_position_before('x'), 9)
        self.assertEqual(tb.insert_position_before('y'), 9)
        self.assertEqual(tb.insert_position_before('y'), 9)

    def test_for_empty_node(self):
        tb = getETB('', 'xyz')

        self.assertEqual(tb.insert_position_before('x'), 0)
        self.assertEqual(tb.insert_position_before('y'), 0)
        self.assertEqual(tb.insert_position_before('z'), 0)

    def test_insert_before_epilogue_block(self):
        tb = getETB('aabbccghixxzz', 'xyz')

        self.assertEqual(tb.insert_position_before(), 9)

if __name__=='__main__':
    unittest.main()
