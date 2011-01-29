#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: cache module
# Created: 29.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import wrap as uncached_wrap

class _WrapCache:
    # Should only used for big expensive objects like tables.
    _cache = {}

    def wrap(self, element):
        key = id(element)
        try:
            return self._cache[key]
        except KeyError:
            wrapped_object = uncached_wrap(element)
        self.add(wrapped_object)
        return wrapped_object

    def add(self, wrapped_object):
        self._cache[id(wrapped_object.xmlnode)] = wrapped_object

    def clear(self):
        self._cache.clear()

_wrapcache = _WrapCache()
wrap = _wrapcache.wrap
clear = _wrapcache.clear
add = _wrapcache.add