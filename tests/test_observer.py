#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test observer object
# Created: 23.01.2011
# Copyright (C) , Manfred Moitzi
# License: GPLv3

# Standard Library
import sys
import unittest

# objects to test
from ezodf.observer import _SimpleObserver

class Listener:
    msg = 'fail'
    def on_save_handler(self, msg):
        self.msg = 'ok'

class TestObserver(unittest.TestCase):
    def setUp(self):
        self.Observer = _SimpleObserver()

    def test_multiple_listeners(self):
        L1 = Listener()
        L2 = Listener()
        self.Observer.subscribe('save', L1)
        self.Observer.subscribe('save', L2)
        self.assertEqual(self.Observer._count_listeners('save'), 2)

    def test_subscribe_event(self):
        listener = Listener()
        self.Observer.subscribe('save', listener)
        self.assertTrue(self.Observer._has_listener('save'))

    def test_subscribe_without_event_handler(self):
        listener = Listener()
        with self.assertRaises(AttributeError):
            self.Observer.subscribe('open', listener)

    def test_unsubscribe_existing_event(self):
        listener = Listener()
        self.Observer.subscribe('save', listener)
        self.Observer.unsubscribe('save', listener)
        self.assertFalse(self.Observer._has_listener('save'))

    def test_unsubscribe_not_existing_event(self):
        listener = Listener()
        with self.assertRaises(KeyError):
            self.Observer.unsubscribe('save', listener)

    def test_unsubscribe_not_existing_listener(self):
        listener = Listener()
        self.Observer.subscribe('save', listener)
        with self.assertRaises(KeyError):
            self.Observer.unsubscribe('save', self)

    def test_broadcast(self):
        listener = Listener()
        self.assertEqual(listener.msg, 'fail')
        self.Observer.subscribe('save', listener)
        self.Observer.broadcast(event='save', msg=self)
        self.assertEqual(listener.msg, 'ok')

    def test_broadcast_without_listeners_is_ok(self):
        self.Observer.broadcast(event='save', msg=self)
        self.assertTrue(True)

    def test_broadcast_to_destroyed_listeners(self):
        listener = Listener()
        self.Observer.subscribe('save', listener)
        del listener
        self.assertEqual(self.Observer._count_listeners('save'), 0)
        self.Observer.broadcast(event='save', msg=self)

if __name__=='__main__':
    unittest.main()