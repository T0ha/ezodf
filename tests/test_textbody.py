#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test TextBody
# Created: 02.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import sys
import unittest

# dependencies
from ezodf.xmlns import etree, CN
from ezodf.nodestructurechecker import StreamTextBodyChecker

# objects to test
from ezodf.body import TextBody

# mocks
class ODFContentMock:
    def __init__(self, tag):
        self.xmlnode = etree.Element(tag)
    @property
    def tag(self):
        return self.xmlnode.tag

class TestStreamTextBody(unittest.TestCase):
    def setUp(self):
        self.body = TextBody()

    def test_empty_body(self):
        result = StreamTextBodyChecker.is_valid(self.body.xmlnode)
        self.assertTrue(result)

    def test_checker_epilogue_error(self):
        body = etree.Element(CN('office:text'))
        body.append(etree.Element(CN('table:dde-links')))
        body.append(etree.Element(CN('text:p')))

        result = StreamTextBodyChecker.is_valid(body)
        self.assertFalse(result)

    def test_checker_prelude_error(self):
        body = etree.Element(CN('office:text'))
        body.append(etree.Element(CN('text:p')))
        body.append(etree.Element(CN('text:user-field-decls')))

        result = StreamTextBodyChecker.is_valid(body)
        self.assertFalse(result)

    def test_append_text_without_epilogue(self):
        body = TextBody()
        body.append(ODFContentMock(CN("text:p")))
        body.append(ODFContentMock(CN("text:h")))
        result = StreamTextBodyChecker.is_valid(body.xmlnode)
        self.assertTrue(result)
        self.assertEqual(body[0].kind, "Paragraph")
        self.assertEqual(body[1].kind, "Heading")

    def test_append_text_with_existing_epilogue(self):
        body = TextBody()
        body.append(ODFContentMock(CN("table:dde-links")))
        body.append(ODFContentMock(CN("text:p")))
        body.append(ODFContentMock(CN("text:h")))

        result = StreamTextBodyChecker.is_valid(body.xmlnode)
        self.assertTrue(result)
        self.assertEqual(body[0].kind, "Paragraph")
        self.assertEqual(body[1].kind, "Heading")


if __name__=='__main__':
    unittest.main()