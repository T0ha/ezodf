#!/usr/bin/env python
#coding:utf-8
# Purpose: testing tools
# Created: 30.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

import os
import random
from lxml import etree

def in_XML(source, target):
    for element in source.strip().split():
        if element not in target:
            return False
    return True

def getdatafile(filename):
    return os.path.join(os.path.dirname(__file__), "data", filename)

SPECFILE = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'specs', 'OpenDocument-v1.1.odt'))
SPECFILE_EXISTS = os.path.exists(SPECFILE)

def get_n_random_tags(count, tags):
    return (random.choice(tags) for _ in range(count))

def create_node(tags):
    nodes = (etree.Element(tag, num=str(num)) for num, tag in enumerate(tags))
    root = etree.Element('root')
    root.extend(nodes)
    return root

class SimpleStructureChecker:
    def __init__(self, prelude_tags, epilogue_tags):
        self.prelude_tags = prelude_tags
        self.epilogue_tags = epilogue_tags

    def has_valid_structure(self, xmlnode):

        def remove_prelude(nodes):
            for tag in self.prelude_tags:
                remove_from_head(tag, nodes)

        def remove_from_head(tag, nodes):
            while nodes[0].tag == tag:
                nodes.pop(0)

        def remove_epilogue(nodes):
            for tag in reversed(self.epilogue_tags):
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
        if has_tags(self.prelude_tags, nodes):
            return False

        remove_epilogue(nodes)
        if has_tags(self.epilogue_tags, nodes):
            return False

        return is_in_creation_order(nodes)
