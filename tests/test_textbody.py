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

class TestStreamTextBody(unittest.TestCase):
    def setUp(self):
        self.body = TextBody()

    def test_empty_body(self):
        result = StreamTextBodyChecker.is_valid(self.body.xmlnode)
        self.assertTrue(result)

    def test_fail_checker(self):
        body = etree.Element(CN('office:text'))
        body.append(etree.Element(CN("table:dde-links")))
        body.append(etree.Element(CN('text:p')))

        result = StreamTextBodyChecker.is_valid(body)
        self.assertFalse(result)

if __name__=='__main__':
    unittest.main()