#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test node organizer
# Created: 31.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import unittest

# test helpers
from mytesttools import create_node

# objects to test
from ezodf.nodeorganizer import EpilogueTagBlock

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
        tree = create_node('aabbccghixxyyzz')
        etb = EpilogueTagBlock(tree, 'xyz')
        self.assertEqual(len(etb), 6)

    def test_get_epilogue_only_tree(self):
        tree = create_node('xxyyzz')
        etb = EpilogueTagBlock(tree, 'xyz')
        self.assertEqual(len(etb), 6)

    def test_get_count_without_eiplogue(self):
        tree = create_node('aabbccghi')
        etb = EpilogueTagBlock(tree, 'xyz')
        self.assertEqual(len(etb), 0)

    def test_get_count_empty_tree(self):
        tree = create_node('')
        etb = EpilogueTagBlock(tree, 'xyz')
        self.assertEqual(len(etb), 0)

    def test_get_count_from_not_well_formed_tree(self):
        tree = create_node('aabbccgxzhi')
        etb = EpilogueTagBlock(tree, 'xyz')
        self.assertEqual(len(etb), 0)

class TestEpilogueTagBlockTagInfo(unittest.TestCase):
    def test_get_tag_info_z(self):
        tree = create_node('aabbccghixxyyzz')
        etb = EpilogueTagBlock(tree, 'xyz')
        start_index, count = etb.tag_info('z')
        self.assertEqual((13, 2), (start_index, count))

    def test_get_tag_info_x(self):
        tree = create_node('aabbccghixxxyyzz')
        etb = EpilogueTagBlock(tree, 'xyz')
        start_index, count = etb.tag_info('x')
        self.assertEqual((9, 3), (start_index, count))

    def test_get_tag_info_for_not_existing_tag(self):
        tree = create_node('aabbccghixxxzz')
        etb = EpilogueTagBlock(tree, 'xyz')
        start_index, count = etb.tag_info('y')
        self.assertEqual((-1, 0), (start_index, count))

    def test_get_tag_info_invalid_tag_error(self):
        tree = create_node('aabbccghixxxzz')
        etb = EpilogueTagBlock(tree, 'xyz')
        with self.assertRaises(ValueError):
            etb.tag_info('w')

    def test_get_tag_info_for_tag_not_in_epilogue(self):
        tree = create_node('aabbccghixxxgyyzz')
        etb = EpilogueTagBlock(tree, 'xyz')
        start_index, count = etb.tag_info('x')
        self.assertEqual((-1, 0), (start_index, count))

class TestEpilogueTagBlockInsertPositionAfter(unittest.TestCase):
    def test_tag_error(self):
        tb = EpilogueTagBlock(create_node('abc'), 'xyz')
        with self.assertRaises(ValueError):
            tb.insert_position_after('d')

    def test_after_existing_tag(self):
        tree = create_node('aabbccghixxyyzz')
        tb = EpilogueTagBlock(tree, 'xyz')

        self.assertEqual(tb.insert_position_after('x'), 11)
        self.assertEqual(tb.insert_position_after('y'), 13)
        self.assertEqual(tb.insert_position_after('z'), 15)

    def test_after_not_existing_tag(self):
        tree = create_node('aabbccghixxzz')
        tb = EpilogueTagBlock(tree, 'xyz')

        self.assertEqual(tb.insert_position_after('x'), 11)
        self.assertEqual(tb.insert_position_after('y'), 11)
        self.assertEqual(tb.insert_position_after('z'), 13)

    def test_without_epilogue(self):
        tree = create_node('aabbccghi')
        tb = EpilogueTagBlock(tree, 'xyz')

        self.assertEqual(tb.insert_position_after('x'), 9)
        self.assertEqual(tb.insert_position_after('y'), 9)
        self.assertEqual(tb.insert_position_after('y'), 9)

    def test_for_empty_node(self):
        tree = create_node('')
        tb = EpilogueTagBlock(tree, 'xyz')

        self.assertEqual(tb.insert_position_after('x'), 0)
        self.assertEqual(tb.insert_position_after('y'), 0)
        self.assertEqual(tb.insert_position_after('z'), 0)

class TestEpilogueTagBlockInsertPositionBefore(unittest.TestCase):
    def test_tag_error(self):
        tb = EpilogueTagBlock(create_node('abc'), 'xyz')
        with self.assertRaises(ValueError):
            tb.insert_position_before('d')

    def test_before_existing_tag(self):
        tree = create_node('aabbccghixxyyzz')
        tb = EpilogueTagBlock(tree, 'xyz')

        self.assertEqual(tb.insert_position_before('x'), 9)
        self.assertEqual(tb.insert_position_before('y'), 11)
        self.assertEqual(tb.insert_position_before('z'), 13)

    def test_before_not_existing_tag(self):
        tree = create_node('aabbccghixxzz')
        tb = EpilogueTagBlock(tree, 'xyz')

        self.assertEqual(tb.insert_position_before('x'), 9)
        self.assertEqual(tb.insert_position_before('y'), 11)
        self.assertEqual(tb.insert_position_before('z'), 11)

    def test_without_epilogue(self):
        tree = create_node('aabbccghi')
        tb = EpilogueTagBlock(tree, 'xyz')

        self.assertEqual(tb.insert_position_before('x'), 9)
        self.assertEqual(tb.insert_position_before('y'), 9)
        self.assertEqual(tb.insert_position_before('y'), 9)

    def test_for_empty_node(self):
        tree = create_node('')
        tb = EpilogueTagBlock(tree, 'xyz')

        self.assertEqual(tb.insert_position_before('x'), 0)
        self.assertEqual(tb.insert_position_before('y'), 0)
        self.assertEqual(tb.insert_position_before('z'), 0)

    def test_insert_before_epilogue_block(self):
        tree = create_node('aabbccghixxzz')
        tb = EpilogueTagBlock(tree, 'xyz')
        self.assertEqual(tb.insert_position_before(), 9)

if __name__=='__main__':
    unittest.main()