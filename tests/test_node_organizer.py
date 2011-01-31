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

PRELUDE_TAGS = ['a', 'b', 'c']
TAGS = ['g', 'h', 'i']
EPILOGUE_TAGS = ['x', 'y', 'z']

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
        no.reorg(tree)
        self.assertTrue(has_valid_structure(tree))

if __name__=='__main__':
    unittest.main()