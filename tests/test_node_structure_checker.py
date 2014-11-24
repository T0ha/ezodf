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
from ezodf.nodeorganizer import PreludeEpilogueOrganizer

# objects to test
from ezodf.nodestructurechecker import NodeStructureChecker


#all tags are single letter tags
PRELUDE_TAGS = 'abc'
EPILOGUE_TAGS = 'xyz'
ALLTAGS = list(PRELUDE_TAGS + 'ghi' + EPILOGUE_TAGS)

checker = SimpleStructureChecker(list(PRELUDE_TAGS), list(EPILOGUE_TAGS))
has_valid_structure = checker.has_valid_structure

class TestNodeStructureChecker(unittest.TestCase):
    def test_valid_content(self):
        node = create_node('aabbccghixxyyzz')
        validator = NodeStructureChecker(PRELUDE_TAGS, 'ghi', EPILOGUE_TAGS)
        self.assertTrue(validator.is_valid(node))

    def test_invalid_content(self):
        node = create_node('aabbccgHixxyyzz')
        validator = NodeStructureChecker(PRELUDE_TAGS, 'ghi', EPILOGUE_TAGS)
        self.assertFalse(validator.is_valid(node))

    def test_valid_content_without_prelude(self):
        node = create_node('ghixxyyzz')
        validator = NodeStructureChecker(PRELUDE_TAGS, 'ghi', EPILOGUE_TAGS)
        self.assertTrue(validator.is_valid(node))

    def test_valid_content_without_epilogue(self):
        node = create_node('aabbccghi')
        validator = NodeStructureChecker(PRELUDE_TAGS, 'ghi', EPILOGUE_TAGS)
        self.assertTrue(validator.is_valid(node))

    def test_valid_content_only_midrange(self):
        node = create_node('ghi')
        validator = NodeStructureChecker(PRELUDE_TAGS, 'ghi', EPILOGUE_TAGS)
        self.assertTrue(validator.is_valid(node))

    def test_valid_content_one_tag(self):
        node = create_node('g')
        validator = NodeStructureChecker(PRELUDE_TAGS, 'ghi', EPILOGUE_TAGS)
        self.assertTrue(validator.is_valid(node))

    def test_valid_content_empty_tag(self):
        node = create_node('')
        validator = NodeStructureChecker(PRELUDE_TAGS, 'ghi', EPILOGUE_TAGS)
        self.assertTrue(validator.is_valid(node))

    def test_reorder(self):
        node = create_node(get_n_random_tags(50, list(PRELUDE_TAGS+'ghi'+EPILOGUE_TAGS)))
        no = PreludeEpilogueOrganizer(PRELUDE_TAGS, EPILOGUE_TAGS)
        no.reorder(node)
        validator = NodeStructureChecker(PRELUDE_TAGS, 'ghi', EPILOGUE_TAGS)

        self.assertEqual(has_valid_structure(node), validator.is_valid(node))


if __name__=='__main__':
    unittest.main()
