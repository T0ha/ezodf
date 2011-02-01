#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test node organizer
# Created: 31.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import unittest
from itertools import chain
import random
from lxml import etree

from ezodf.nodeorganizer import PreludeEpilogueOrganizer
from ezodf.nodeorganizer import PreludeTagBlock
from ezodf.nodeorganizer import EpilogueTagBlock

#all tags are single letter tags
PRELUDE_TAGS = 'abc'
TAGS = 'ghi'
EPILOGUE_TAGS = 'xyz'

ALLTAGS = list(chain(PRELUDE_TAGS, TAGS, EPILOGUE_TAGS))

def get_n_random_tags(count, tags):
    return (random.choice(tags) for _ in range(count))

def create_tree(tags):
    nodes = (etree.Element(tag, num=str(num)) for num, tag in enumerate(tags))
    root = etree.Element('root')
    root.extend(nodes)
    return root

def has_valid_structure(xmlnode):

    def remove_prelude(nodes):
        for tag in PRELUDE_TAGS:
            remove_from_head(tag, nodes)

    def remove_from_head(tag, nodes):
        while nodes[0].tag == tag:
            nodes.pop(0)

    def remove_epilogue(nodes):
        for tag in reversed(EPILOGUE_TAGS):
            remove_from_tail(tag, nodes)

    def remove_from_tail(tag, nodes):
        while nodes[-1].tag == tag:
            nodes.pop()

    def has_tags(tags, nodes):
        def has_tag(tag):
            for node in nodes:
                if node.tag == tag:
                    return True
            return False

        for tag in tags:
            if has_tag(tag):
                return True
        return False

    def is_in_creation_order(nodes):
        sorted_nodes = sorted(nodes, key=lambda n: int(n.get('num')))
        for node1, node2 in zip(nodes, sorted_nodes):
            if node1.tag != node2.tag or \
               node1.get('num') != node2.get('num'):
                return False
        return True

    nodes = xmlnode.getchildren()

    remove_prelude(nodes)
    if has_tags(PRELUDE_TAGS, nodes):
        return False

    remove_epilogue(nodes)
    if has_tags(EPILOGUE_TAGS, nodes):
        return False

    return is_in_creation_order(nodes)

class TestTestFunction(unittest.TestCase):
    def test_valid_structure_sorted_midrange(self):
        nodes = create_tree('aabbcc' 'ghi' 'xxxyyzz')
        self.assertTrue(has_valid_structure(nodes))

    def test_valid_structure_unsorted_midrange(self):
        nodes = create_tree('aabbcc' 'ihg' 'xxxyyzz')
        self.assertTrue(has_valid_structure(nodes))

    def test_invalid_structure_b_after_c(self):
        nodes = create_tree('aabbcb' 'ghi' 'xxxyyzz')
        self.assertFalse(has_valid_structure(nodes))

    def test_invalid_structure_x_after_y(self):
        nodes = create_tree('aabbcc' 'ghi' 'xxyxyzz')
        self.assertFalse(has_valid_structure(nodes))

    def test_invalid_structure_a_in_midrange(self):
        nodes = create_tree('aabccc' 'gahi' 'xxxyyzz')
        self.assertFalse(has_valid_structure(nodes))

    def test_invalid_structure_a_in_midrange_without_prelude(self):
        nodes = create_tree('gahi' 'xxxyyzz')
        self.assertFalse(has_valid_structure(nodes))

    def test_invalid_structure_x_in_midrange(self):
        nodes = create_tree('aabccc' 'gxhi' 'xxxyyzz')
        self.assertFalse(has_valid_structure(nodes))

    def test_invalid_structure_x_in_midrange_without_epilouge(self):
        nodes = create_tree('aabccc' 'gxhi')
        self.assertFalse(has_valid_structure(nodes))

class TestPreludeEpilogueOrganizer(unittest.TestCase):
    def test_reorg(self):
        tags = get_n_random_tags(100, ALLTAGS)
        tree = create_tree(tags)

        no = PreludeEpilogueOrganizer(PRELUDE_TAGS, EPILOGUE_TAGS)
        no.reorder(tree)
        self.assertTrue(has_valid_structure(tree))

class TestPreludeTagBlockBasics(unittest.TestCase):
    def test_xmlnode_is_none_error(self):
        with self.assertRaises(ValueError):
            PreludeTagBlock(None, '')

    def test_unique_order_tags(self):
        with self.assertRaises(ValueError):
            PreludeTagBlock(create_tree('abc'), 'abcc')

    def test_all_tags_exist(self):
        tree = create_tree('aabbccghixyz')
        ptb = PreludeTagBlock(tree, PRELUDE_TAGS)
        self.assertEqual(len(ptb), 6)

    def test_prelude_only_tree(self):
        tree = create_tree('aabbcc')
        ptb = PreludeTagBlock(tree, PRELUDE_TAGS)
        self.assertEqual(len(ptb), 6)

    def test_without_prelude(self):
        tree = create_tree('ghixyz')
        ptb = PreludeTagBlock(tree, PRELUDE_TAGS)
        self.assertEqual(len(ptb), 0)

    def test_empty_tree(self):
        tree = create_tree('')
        ptb = PreludeTagBlock(tree, PRELUDE_TAGS)
        self.assertEqual(len(ptb), 0)

    def test_from_not_well_formed_tree(self):
        tree = create_tree('haabbccghixyz')
        ptb = PreludeTagBlock(tree, PRELUDE_TAGS)
        self.assertEqual(len(ptb), 0)

class TestPreludeTagBlockInfo(unittest.TestCase):
    def test_tag_info_a(self):
        tree = create_tree('aabbccghixyz')
        ptb = PreludeTagBlock(tree, PRELUDE_TAGS)
        start_index, count = ptb.tag_info('a')
        self.assertEqual((0, 2), (start_index, count))

    def test_tag_info_b(self):
        tree = create_tree('aabbbccghixyz')
        ptb = PreludeTagBlock(tree, PRELUDE_TAGS)
        start_index, count = ptb.tag_info('b')
        self.assertEqual((2, 3), (start_index, count))

    def test_tag_info_for_not_existing_tag(self):
        tree = create_tree('aabbbghixyz')
        ptb = PreludeTagBlock(tree, PRELUDE_TAGS)
        start_index, count = ptb.tag_info('c')
        self.assertEqual((-1, 0), (start_index, count))

    def test_tag_info_invalid_tag_error(self):
        tree = create_tree('aabbbghixyz')
        ptb = PreludeTagBlock(tree, PRELUDE_TAGS)
        with self.assertRaises(ValueError):
            ptb.tag_info('d')

    def test_tag_info_tag_not_in_prelude_block(self):
        tree = create_tree('aabbbgccixyz')
        ptb = PreludeTagBlock(tree, PRELUDE_TAGS)
        start_index, count = ptb.tag_info('c')
        self.assertEqual((-1, 0), (start_index, count))

class TestPreludeTagBlockInsertPositionBefore(unittest.TestCase):
    def test_tag_error(self):
        tree = create_tree('aabbccghixxyyzz')
        tb = PreludeTagBlock(tree, PRELUDE_TAGS)
        with self.assertRaises(ValueError):
            tb.insert_position_before('d')

    def test_before_existing_tag(self):
        tree = create_tree('aabbccghixxyyzz')
        tb = PreludeTagBlock(tree, PRELUDE_TAGS)

        self.assertEqual(tb.insert_position_before('a'), 0)
        self.assertEqual(tb.insert_position_before('b'), 2)
        self.assertEqual(tb.insert_position_before('c'), 4)

    def test_before_not_existing_tag(self):
        tree = create_tree('aaccghixxyyzz')
        tb = PreludeTagBlock(tree, PRELUDE_TAGS)

        self.assertEqual(tb.insert_position_before('a'), 0)
        self.assertEqual(tb.insert_position_before('b'), 2)
        self.assertEqual(tb.insert_position_before('c'), 2)

    def test_without_prelude(self):
        tree = create_tree('ghixxyyzz')
        tb = PreludeTagBlock(tree, PRELUDE_TAGS)

        self.assertEqual(tb.insert_position_before('a'), 0)
        self.assertEqual(tb.insert_position_before('b'), 0)
        self.assertEqual(tb.insert_position_before('c'), 0)

    def test_for_empty_node(self):
        tree = create_tree('')
        tb = PreludeTagBlock(tree, PRELUDE_TAGS)

        self.assertEqual(tb.insert_position_before('a'), 0)
        self.assertEqual(tb.insert_position_before('b'), 0)
        self.assertEqual(tb.insert_position_before('c'), 0)

class TestPreludeTagBlockInsertPositionAfter(unittest.TestCase):
    def test_tag_error(self):
        tree = create_tree('aabbccghixxyyzz')
        tb = PreludeTagBlock(tree, PRELUDE_TAGS)
        with self.assertRaises(ValueError):
            tb.insert_position_after('d')

    def test_after_existing_tag(self):
        tree = create_tree('aabbccghixxyyzz')
        tb = PreludeTagBlock(tree, PRELUDE_TAGS)

        self.assertEqual(tb.insert_position_after('a'), 2)
        self.assertEqual(tb.insert_position_after('b'), 4)
        self.assertEqual(tb.insert_position_after('c'), 6)

    def test_after_not_existing_tag(self):
        tree = create_tree('aaccghixxyyzz')
        tb = PreludeTagBlock(tree, PRELUDE_TAGS)

        self.assertEqual(tb.insert_position_after('a'), 2)
        self.assertEqual(tb.insert_position_after('b'), 2)
        self.assertEqual(tb.insert_position_after('c'), 4)

    def test_without_prelude(self):
        tree = create_tree('ghixxyyzz')
        tb = PreludeTagBlock(tree, PRELUDE_TAGS)

        self.assertEqual(tb.insert_position_after('a'), 0)
        self.assertEqual(tb.insert_position_after('b'), 0)
        self.assertEqual(tb.insert_position_after('c'), 0)

    def test_for_empty_node(self):
        tree = create_tree('')
        tb = PreludeTagBlock(tree, PRELUDE_TAGS)

        self.assertEqual(tb.insert_position_after('a'), 0)
        self.assertEqual(tb.insert_position_after('b'), 0)
        self.assertEqual(tb.insert_position_after('c'), 0)


class TestEpilogueTagBlockBasics(unittest.TestCase):
    def test_xmlnode_is_none_error(self):
        with self.assertRaises(ValueError):
            EpilogueTagBlock(None, '')

    def test_unique_order_tags(self):
        with self.assertRaises(ValueError):
            EpilogueTagBlock(create_tree('abc'), 'abcc')

    def test_get_count(self):
        tree = create_tree('aabbccghixxyyzz')
        etb = EpilogueTagBlock(tree, EPILOGUE_TAGS)
        self.assertEqual(len(etb), 6)

    def test_get_epilogue_only_tree(self):
        tree = create_tree('xxyyzz')
        etb = EpilogueTagBlock(tree, EPILOGUE_TAGS)
        self.assertEqual(len(etb), 6)

    def test_get_count_without_eiplogue(self):
        tree = create_tree('aabbccghi')
        etb = EpilogueTagBlock(tree, EPILOGUE_TAGS)
        self.assertEqual(len(etb), 0)

    def test_get_count_empty_tree(self):
        tree = create_tree('')
        etb = EpilogueTagBlock(tree, EPILOGUE_TAGS)
        self.assertEqual(len(etb), 0)

    def test_get_count_from_not_well_formed_tree(self):
        tree = create_tree('aabbccgxzhi')
        etb = EpilogueTagBlock(tree, EPILOGUE_TAGS)
        self.assertEqual(len(etb), 0)

class TestEpilogueTagBlockTagInfo(unittest.TestCase):
    def test_get_tag_info_z(self):
        tree = create_tree('aabbccghixxyyzz')
        etb = EpilogueTagBlock(tree, EPILOGUE_TAGS)
        start_index, count = etb.tag_info('z')
        self.assertEqual((13, 2), (start_index, count))

    def test_get_tag_info_x(self):
        tree = create_tree('aabbccghixxxyyzz')
        etb = EpilogueTagBlock(tree, EPILOGUE_TAGS)
        start_index, count = etb.tag_info('x')
        self.assertEqual((9, 3), (start_index, count))

    def test_get_tag_info_for_not_existing_tag(self):
        tree = create_tree('aabbccghixxxzz')
        etb = EpilogueTagBlock(tree, EPILOGUE_TAGS)
        start_index, count = etb.tag_info('y')
        self.assertEqual((-1, 0), (start_index, count))

    def test_get_tag_info_invalid_tag_error(self):
        tree = create_tree('aabbccghixxxzz')
        etb = EpilogueTagBlock(tree, EPILOGUE_TAGS)
        with self.assertRaises(ValueError):
            etb.tag_info('w')

    def test_get_tag_info_for_tag_not_in_epilogue(self):
        tree = create_tree('aabbccghixxxgyyzz')
        etb = EpilogueTagBlock(tree, EPILOGUE_TAGS)
        start_index, count = etb.tag_info('x')
        self.assertEqual((-1, 0), (start_index, count))

class TestEpilogueTagBlockInsertPositionAfter(unittest.TestCase):
    def test_tag_error(self):
        tb = EpilogueTagBlock(create_tree('abc'), EPILOGUE_TAGS)
        with self.assertRaises(ValueError):
            tb.insert_position_after('d')

    def test_after_existing_tag(self):
        tree = create_tree('aabbccghixxyyzz')
        tb = EpilogueTagBlock(tree, EPILOGUE_TAGS)

        self.assertEqual(tb.insert_position_after('x'), 11)
        self.assertEqual(tb.insert_position_after('y'), 13)
        self.assertEqual(tb.insert_position_after('z'), 15)

    def test_after_not_existing_tag(self):
        tree = create_tree('aabbccghixxzz')
        tb = EpilogueTagBlock(tree, EPILOGUE_TAGS)

        self.assertEqual(tb.insert_position_after('x'), 11)
        self.assertEqual(tb.insert_position_after('y'), 11)
        self.assertEqual(tb.insert_position_after('z'), 13)

    def test_without_epilogue(self):
        tree = create_tree('aabbccghi')
        tb = EpilogueTagBlock(tree, EPILOGUE_TAGS)

        self.assertEqual(tb.insert_position_after('x'), 9)
        self.assertEqual(tb.insert_position_after('y'), 9)
        self.assertEqual(tb.insert_position_after('y'), 9)

    def test_for_empty_node(self):
        tree = create_tree('')
        tb = EpilogueTagBlock(tree, EPILOGUE_TAGS)

        self.assertEqual(tb.insert_position_after('x'), 0)
        self.assertEqual(tb.insert_position_after('y'), 0)
        self.assertEqual(tb.insert_position_after('z'), 0)

class TestEpilogueTagBlockInsertPositionBefore(unittest.TestCase):
    def test_tag_error(self):
        tb = EpilogueTagBlock(create_tree('abc'), EPILOGUE_TAGS)
        with self.assertRaises(ValueError):
            tb.insert_position_before('d')

    def test_before_existing_tag(self):
        tree = create_tree('aabbccghixxyyzz')
        tb = EpilogueTagBlock(tree, EPILOGUE_TAGS)

        self.assertEqual(tb.insert_position_before('x'), 9)
        self.assertEqual(tb.insert_position_before('y'), 11)
        self.assertEqual(tb.insert_position_before('z'), 13)

    def test_before_not_existing_tag(self):
        tree = create_tree('aabbccghixxzz')
        tb = EpilogueTagBlock(tree, EPILOGUE_TAGS)

        self.assertEqual(tb.insert_position_before('x'), 9)
        self.assertEqual(tb.insert_position_before('y'), 11)
        self.assertEqual(tb.insert_position_before('z'), 11)

    def test_without_epilogue(self):
        tree = create_tree('aabbccghi')
        tb = EpilogueTagBlock(tree, EPILOGUE_TAGS)

        self.assertEqual(tb.insert_position_before('x'), 9)
        self.assertEqual(tb.insert_position_before('y'), 9)
        self.assertEqual(tb.insert_position_before('y'), 9)

    def test_for_empty_node(self):
        tree = create_tree('')
        tb = EpilogueTagBlock(tree, EPILOGUE_TAGS)

        self.assertEqual(tb.insert_position_before('x'), 0)
        self.assertEqual(tb.insert_position_before('y'), 0)
        self.assertEqual(tb.insert_position_before('z'), 0)

if __name__=='__main__':
    unittest.main()