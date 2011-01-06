#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: BaseClass for ODF content objects
# Created: 03.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import etree, register_class, to_object

def safelen(text):
    # can handle `None` as input
    return len(text) if text else 0

@register_class
class BaseClass:
    TAG = 'BaseClass'

    def __init__(self, xmlroot=None):
        if xmlroot is not None:
            self.xmlroot = xmlroot
        else:
            self.xmlroot = etree.Element(self.TAG)

    def __iter__(self):
        for element in self.xmlroot.iterchildren():
            yield to_object(element)

    def __len__(self):
        """ Get count of children """
        return len(self.xmlroot)

    @property
    def text(self):
        return self.xmlroot.text
    @text.setter
    def text(self, value):
        self.xmlroot.text = value

    @property
    def tail(self):
        return self.xmlroot.tail
    @tail.setter
    def tail(self, value):
        self.xmlroot.tail = value

    ## Index operations

    def __getitem__(self, index):
        """ Get the child at position `index` as wrapped class.

        :param int index: child position
        :returns: WrapperClass
        """
        return self.get(index)

    def __setitem__(self, index, element):
        """ Set (replace) the child at position `index` by element.

        :param int index: child position
        :param aWrapperClass element: new child node
        """
        found = self.xmlroot[int(index)]
        self.xmlroot.replace(found, element.xmlroot)

    def __delitem__(self, index):
        """ Delete child at position `index`.

        :param int index: child position
        """
        del self.xmlroot[int(index)]

    def index(self, child):
        """ Get numeric index of `child`.

        :param WrapperClass child: get index for this child
        :returns: int
        """
        return self.xmlroot.index(child.xmlroot)

    def insert(self, index, child):
        """ Insert child at position `index`.

        :param int index: insert position for child
        :param WrapperClass child: child to insert
        :returns: WrappedClass child
        """
        self.xmlroot.insert(int(index), child.xmlroot)
        return child # pass through

    def get(self, index):
        """ Get children at `index` as wrapped object.

        :param int index: child position
        :returns: WrapperClass
        """
        xmlelement = self.xmlroot[int(index)]
        return to_object(xmlelement)

    ## Attribute access for the xmlroot element

    def getattr(self, key, default=None):
        """ Get the `key` attribute value of the xmlroot element or `default`
        if `key` does not exist.

        :param str key: name of key
        :param default: default value if `key` not found
        :return: str
        """
        value = self.xmlroot.get(key)
        if value is None:
            value = default
        return value

    def setattr(self, key, value):
        """ Set the `key` attribute of the xmlroot element to `value`.

        :param str key: name of key
        :param value: value for key
        """
        if value:
            self.xmlroot.set(key, str(value))
        else:
            raise ValueError(value)

    ## List operations

    def add(self, child, insert_before=None):
        """ Add `child` as to node.

        :param WrapperClass child: child to insert/append
        :param WrapperClass insert_before: insert child before `insert_before`
        :returns: WrappedClass child
        """
        if insert_before is not None:
            position = self.index(insert_before)
            self.insert(position, child)
        else:
            self.xmlroot.append(child.xmlroot)
        return child # pass through

    def remove(self, child):
        """ Remove `child` object from node.

        :param WrapperClass child: child to remove
        """
        self.xmlroot.remove(child.xmlroot)

    def clear(self):
        """ Remove all content from node. """
        self.xmlroot.clear()

    ## production code

    @property
    def textlen(self):
        """ Returns the character count of the plain text content as int. """
        # default implementation, does not respect child elements
        return safelen(self.xmlroot.text)

    def plaintext(self):
        """ Get content of node as plain (unformatted) text string. """
        # default implementation, does not respect child elements
        text = self.xmlroot.text
        return text if text else ""

    def element_at_cursorpos(self, pos):
        """ Find element at `pos`, where `pos` is relative to the elements start.

        :returns: tuple (element, cursorpos-relative-to-element-start) or (None, None)
        """
        # basic function for text navigation ???
        # pos in element.text ... return (self, pos)
        # pos in child of element ... ok  (child, pos - start-of-child)
        # how to deal with text in child.tail
        raise NotImplemented

