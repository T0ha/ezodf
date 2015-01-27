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
from ezodf.nodeorganizer import PreludeTagBlock

def getPTB(nodes, preludetags='abc'):
    return PreludeTagBlock(create_node(nodes), preludetags)

class CounterAdapter:
    def __init__(self, tags='abc'):
        self.tags = list(tags)

    def count(self, nodes):
        prelude = PreludeTagBlock(create_node(nodes), self.tags)
        return len(prelude)

class TestPreludeTagBlockLen(unittest.TestCase):
    def setUp(self):
        self.ptb = CounterAdapter(list('abc'))

    def test_aabbcc(self):
        self.assertEqual(self.ptb.count('aabbccddeeff'), 6)

    def test_bbcc(self):
        self.assertEqual(self.ptb.count('bbccddeeff'), 4)

    def test_cc(self):
        self.assertEqual(self.ptb.count('ccddeeff'), 2)

    def test_only_aa(self):
        self.assertEqual(self.ptb.count('aa'), 2)

    def test_only_bb(self):
        self.assertEqual(self.ptb.count('bb'), 2)

    def test_only_cc(self):
        self.assertEqual(self.ptb.count('cc'), 2)

    def test_no_tags(self):
        self.assertEqual(self.ptb.count(''), 0)

    def test_no_matches(self):
        self.assertEqual(self.ptb.count('ddeeff'), 0)

    def test_invalid_prelude(self):
        self.assertEqual(self.ptb.count('dadeeff'), 0)


class TestPreludeTagBlockBasics(unittest.TestCase):
    def test_xmlnode_is_none_error(self):
        with self.assertRaises(ValueError):
            PreludeTagBlock(None, '')

    def test_no_prelude_tags(self):
        with self.assertRaises(ValueError):
            PreludeTagBlock(create_node('abc'), '')

    def test_unique_order_tags(self):
        with self.assertRaises(ValueError):
            PreludeTagBlock(create_node('abc'), 'abcc')

    def test_all_tags_exist(self):
        ptb = getPTB('aabbccghixyz')
        self.assertEqual(len(ptb), 6)

    def test_only_aa(self):
        ptb = getPTB('aaghixyz')
        self.assertEqual(len(ptb), 2)

    def test_only_bb(self):
        ptb = getPTB('bbghixyz')
        self.assertEqual(len(ptb), 2)

    def test_only_cc(self):
        ptb = getPTB('ccghixyz')
        self.assertEqual(len(ptb), 2)

    def test_prelude_only_tree(self):
        ptb = getPTB('aabbcc')
        self.assertEqual(len(ptb), 6)

    def test_without_prelude(self):
        ptb = getPTB('ghixyz')
        self.assertEqual(len(ptb), 0)

    def test_empty_tree(self):
        ptb = getPTB('')
        self.assertEqual(len(ptb), 0)

    def test_from_not_well_formed_tree(self):
        ptb = getPTB('haabbccghixyz')
        self.assertEqual(len(ptb), 0)

class TestPreludeTagBlockInfo(unittest.TestCase):
    def test_tag_info_a(self):
        ptb = getPTB('aabbccghixyz')
        start_index, count = ptb.tag_info('a')
        self.assertEqual((0, 2), (start_index, count))

    def test_tag_info_b(self):
        ptb = getPTB('aabbbccghixyz')
        start_index, count = ptb.tag_info('b')
        self.assertEqual((2, 3), (start_index, count))

    def test_tag_info_for_not_existing_tag(self):
        ptb = getPTB('aabbbghixyz')
        start_index, count = ptb.tag_info('c')
        self.assertEqual((-1, 0), (start_index, count))

    def test_tag_info_invalid_tag_error(self):
        ptb = getPTB('aabbbghixyz')
        with self.assertRaises(ValueError):
            ptb.tag_info('d')

    def test_tag_info_tag_not_in_prelude_block(self):
        ptb = getPTB('aabbbgccixyz')
        start_index, count = ptb.tag_info('c')
        self.assertEqual((-1, 0), (start_index, count))

class TestPreludeTagBlockInsertPositionBefore(unittest.TestCase):
    def test_tag_error(self):
        tb = getPTB('aabbccghixxyyzz')
        with self.assertRaises(ValueError):
            tb.insert_position_before('d')

    def test_before_existing_tag(self):
        tb = getPTB('aabbccghixxyyzz')

        self.assertEqual(tb.insert_position_before('a'), 0)
        self.assertEqual(tb.insert_position_before('b'), 2)
        self.assertEqual(tb.insert_position_before('c'), 4)

    def test_before_not_existing_tag(self):
        tb = getPTB('aaccghixxyyzz')

        self.assertEqual(tb.insert_position_before('a'), 0)
        self.assertEqual(tb.insert_position_before('b'), 2)
        self.assertEqual(tb.insert_position_before('c'), 2)

    def test_without_prelude(self):
        tb = getPTB('ghixxyyzz')

        self.assertEqual(tb.insert_position_before('a'), 0)
        self.assertEqual(tb.insert_position_before('b'), 0)
        self.assertEqual(tb.insert_position_before('c'), 0)

    def test_for_empty_node(self):
        tb = getPTB('')

        self.assertEqual(tb.insert_position_before('a'), 0)
        self.assertEqual(tb.insert_position_before('b'), 0)
        self.assertEqual(tb.insert_position_before('c'), 0)

class TestPreludeTagBlockInsertPositionAfter(unittest.TestCase):
    def test_tag_error(self):
        tb = getPTB('aabbccghixxyyzz')
        with self.assertRaises(ValueError):
            tb.insert_position_after('d')

    def test_after_existing_tag(self):
        tb = getPTB('aabbccghixxyyzz')

        self.assertEqual(tb.insert_position_after('a'), 2)
        self.assertEqual(tb.insert_position_after('b'), 4)
        self.assertEqual(tb.insert_position_after('c'), 6)

    def test_after_not_existing_tag(self):
        tb = getPTB('aaccghixxyyzz')

        self.assertEqual(tb.insert_position_after('a'), 2)
        self.assertEqual(tb.insert_position_after('b'), 2)
        self.assertEqual(tb.insert_position_after('c'), 4)

    def test_without_prelude(self):
        tb = getPTB('ghixxyyzz')

        self.assertEqual(tb.insert_position_after('a'), 0)
        self.assertEqual(tb.insert_position_after('b'), 0)
        self.assertEqual(tb.insert_position_after('c'), 0)

    def test_for_empty_node(self):
        tb = getPTB('')

        self.assertEqual(tb.insert_position_after('a'), 0)
        self.assertEqual(tb.insert_position_after('b'), 0)
        self.assertEqual(tb.insert_position_after('c'), 0)

    def test_after_all_prelude_tags(self):
        tb = getPTB('aabbccghixxyyzz')

        self.assertEqual(tb.insert_position_after(), 6)

if __name__=='__main__':
    unittest.main()
