#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: caching module
# Created: 22.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from weakref import WeakSet

class SimpleObserver:
    """ Used to inform objects to write back cached values.

    Using WeakSet as container, removing of listeners is not
    necessary.
    """

    def __init__(self):
        self._listeners = WeakSet()

    def register(self, listener_method):
        self._listeners.add(listener_method)

    def update(self):
        for listener_method in self._listeners:
            listener_method()

