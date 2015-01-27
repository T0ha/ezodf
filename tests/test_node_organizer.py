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
from mytesttools import SimpleStructureChecker, create_node, get_n_random_tags

# objects to test
from ezodf.nodeorganizer import PreludeEpilogueOrganizer

#all tags are single letter tags
PRELUDE_TAGS = 'abc'
EPILOGUE_TAGS = 'xyz'
ALLTAGS = list(PRELUDE_TAGS + 'ghi' + EPILOGUE_TAGS)

checker = SimpleStructureChecker(list(PRELUDE_TAGS), list(EPILOGUE_TAGS))
has_valid_structure = checker.has_valid_structure

class TestTestFunction(unittest.TestCase):
    def test_valid_structure_sorted_midrange(self):
        nodes = create_node('aabbcc' 'ghi' 'xxxyyzz')
        self.assertTrue(has_valid_structure(nodes))

    def test_valid_structure_unsorted_midrange(self):
        nodes = create_node('aabbcc' 'ihg' 'xxxyyzz')
        self.assertTrue(has_valid_structure(nodes))

    def test_invalid_structure_b_after_c(self):
        nodes = create_node('aabbcb' 'ghi' 'xxxyyzz')
        self.assertFalse(has_valid_structure(nodes))

    def test_invalid_structure_x_after_y(self):
        nodes = create_node('aabbcc' 'ghi' 'xxyxyzz')
        self.assertFalse(has_valid_structure(nodes))

    def test_invalid_structure_a_in_midrange(self):
        nodes = create_node('aabccc' 'gahi' 'xxxyyzz')
        self.assertFalse(has_valid_structure(nodes))

    def test_invalid_structure_a_in_midrange_without_prelude(self):
        nodes = create_node('gahi' 'xxxyyzz')
        self.assertFalse(has_valid_structure(nodes))

    def test_invalid_structure_x_in_midrange(self):
        nodes = create_node('aabccc' 'gxhi' 'xxxyyzz')
        self.assertFalse(has_valid_structure(nodes))

    def test_invalid_structure_x_in_midrange_without_epilouge(self):
        nodes = create_node('aabccc' 'gxhi')
        self.assertFalse(has_valid_structure(nodes))

class TestPreludeEpilogueOrganizer(unittest.TestCase):
    def setUp(self):
        self.nodeorganizer = PreludeEpilogueOrganizer(PRELUDE_TAGS, EPILOGUE_TAGS)

    def test_reorg(self):
        tags = get_n_random_tags(100, ALLTAGS)
        tree = create_node(tags)
        self.nodeorganizer.reorder(tree)
        self.assertTrue(has_valid_structure(tree))

    def test_reorg_with_zero_nodes(self):
        node = create_node('')
        self.nodeorganizer.reorder(node)
        self.assertEqual(0, len(node))

    def test_reorg_with_one_node(self):
        node = create_node('g')
        self.nodeorganizer.reorder(node)
        self.assertEqual('g', node[0].tag)

if __name__=='__main__':
    unittest.main()
