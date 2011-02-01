#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test exceptions
# Created: 01.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import unittest

from ezodf.exceptions import NodeContentError

def raise_NodeContentError():
    raise NodeContentError('test', 'testnode')

class TestNodeContentError(unittest.TestCase):
    def test_raise(self):
        try:
            raise_NodeContentError()
        except NodeContentError as err:
            self.assertEqual(err.msg, 'test')
            self.assertEqual(err.xmlnode, 'testnode')

if __name__=='__main__':
    unittest.main()