#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: GenericWrapper for ODF content objects
# Created: 03.01.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .xmlns import etree, register_class, wrap

def safelen(text):
    # can handle `None` as input
    return len(text) if text else 0

@register_class
class GenericWrapper:
    TAG = 'GenericWrapper'

    def __init__(self, xmlnode=None):
        if xmlnode is not None:
            self.xmlnode = xmlnode
        else:
            self.xmlnode = etree.Element(self.TAG)

    def __iter__(self):
        for element in self.xmlnode.iterchildren():
            yield wrap(element)

    def __len__(self):
        """ Get count of children """
        return len(self.xmlnode)

    @property
    def text(self):
        return self.xmlnode.text
    @text.setter
    def text(self, value):
        self.xmlnode.text = value

    @property
    def tail(self):
        return self.xmlnode.tail
    @tail.setter
    def tail(self, value):
        self.xmlnode.tail = value

    ## Index operations

    def __getitem__(self, index):
        return self.get_child(index)
    def __setitem__(self, index, element):
        self.set_child(index, element)
    def __delitem__(self, index):
        self.del_child(index)

    def index(self, child):
        """ Get numeric index of `child`.

        :param WrapperClass child: get index for this child
        :returns: int
        """
        return self.xmlnode.index(child.xmlnode)

    def insert(self, index, child):
        """ Insert child at position `index`.

        :param int index: insert position for child
        :param WrapperClass child: child to insert
        :returns: WrappedClass child
        """
        self.xmlnode.insert(int(index), child.xmlnode)
        return child # pass through

    def get_child(self, index):
        """ Get children at `index` as wrapped object.

        :param int index: child position
        :returns: WrapperClass
        """
        xmlelement = self.xmlnode[int(index)]
        return wrap(xmlelement)

    def set_child(self, index, element):
        """ Set (replace) the child at position `index` by element.

        :param int index: child position
        :param WrapperClass element: new child node
        """
        found = self.xmlnode[int(index)]
        self.xmlnode.replace(found, element.xmlnode)

    def del_child(self, index):
        """ Delete child at position `index`.

        :param int index: child position
        """
        del self.xmlnode[int(index)]

    ## Attribute access for the xmlnode element

    def get_attr(self, key, default=None):
        """ Get the `key` attribute value of the xmlnode element or `default`
        if `key` does not exist.

        :param str key: name of key
        :param default: default value if `key` not found
        :return: str
        """
        value = self.xmlnode.get(key)
        if value is None:
            value = default
        return value

    def set_attr(self, key, value):
        """ Set the `key` attribute of the xmlnode element to `value`.

        :param str key: name of key
        :param value: value for key
        """
        if value:
            self.xmlnode.set(key, str(value))
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
            self.xmlnode.append(child.xmlnode)
        return child # pass through

    def remove(self, child):
        """ Remove `child` object from node.

        :param WrapperClass child: child to remove
        """
        self.xmlnode.remove(child.xmlnode)

    def clear(self):
        """ Remove all content from node. """
        self.xmlnode.clear()

    ## production code

    @property
    def textlen(self):
        """ Returns the character count of the plain text content as int. """
        # default implementation, does not respect child elements
        return safelen(self.xmlnode.text)

    def plaintext(self):
        """ Get content of node as plain (unformatted) text string. """
        # default implementation, does not respect child elements
        text = self.xmlnode.text
        return text if text else ""

