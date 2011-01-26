.. module:: base

GenericWrapper Class
====================

.. class:: GenericWrapper(xmlnode=None)

   :class:`GenericWrapper` wrappes an :class:`lxml.Element` object. If
   `xmlnode` is `None` a new node with elementname :attr:`~GenericWrapper.TAG`
   will be created.

   All output nodes are wrapped into :class:`GenericWrapper` or a subclass
   of it and also all input nodes.

   All wrapping classes are stored by the :func:`~xmlns.register_class`
   function in a central register. The :func:`~xmlns.wrap` function searches
   by the `tag` attribute of the :class:`lxml.Element` for the appropriate
   wrapping class, calls this class `cls(xmlnode=element)` and returns the
   resulting object.

Attributes
----------

.. attribute:: GenericWrapper.TAG (read)

   Tag name of the wrapped XML element (like <text:p>) in Clark Notation.
   To get the Clark Notation of an element use the :func:`xmlns.CN` function.

.. attribute:: GenericWrapper.xmlnode (read)

   Reference to the :class:`lxml.Element` object.

.. attribute:: GenericWrapper.text (read/write)

   Get/Set the :attr:`lxml.Element.text` content as `str`.

.. attribute:: GenericWrapper.tail (read/write)

   Get/Set the :attr:`lxml.Element.tail` content as `str`.

.. attribute:: GenericWrapper.textlen (read)

   Should return the length of the :func:`~GenericWrapper.plaintext` result.

.. attribute:: GenericWrapper.kind (read)

   Get the class name as `str`. (eg. ``'GenericWrapper'`` for this class)

Methods
-------

.. method:: GenericWrapper.__init__(xmlnode=None)

.. method:: GenericWrapper.__iter__()

   Iterate over all child nodes, yields `wrapped` XML nodes.

.. method:: GenericWrapper.__len__()

   Get count of child nodes.

.. method:: GenericWrapper.__getitem__(index)

   :param int index: numeric index

   Get `wrapped` XML child-node at position `index`.

.. method:: GenericWrapper.__setitem__(index, element)

   :param int index: numeric index
   :param GenericWrapper element: wrapped XML node

   Set child at position `index` to element.

.. method:: GenericWrapper.__delitem__(index)

   :param int index: numeric index

   Delete child at position `index`.

.. method:: GenericWrapper.index(child)

   :param GenericWrapper child: wrapped XML node

   Get numeric index of `child` as `int`.

   Raises `IndexError` if :attr:`child.xmlnode` is not in :attr:`self.xmlnode`

.. method:: GenericWrapper.insert(index, child)

   :param GenericWrapper child: wrapped XML node

.. method:: GenericWrapper.get_child(index)

   :param int index: numeric index
   :returns: wrapped XML node

   Get `wrapped` XML node at position `index`.

.. method:: GenericWrapper.set_child(index, element)

   :param int index: numeric index
   :param GenericWrapper element: wrapped XML node

.. method:: GenericWrapper.del_child(index)

   :param int index: numeric index

   Remove XML node at position `index`.

.. method:: GenericWrapper.findall(tag)

   :param str tag: tag name in Clark Notation

   Find all subelements by xml-tag (in Clark Notation).

.. method:: GenericWrapper.get_attr(key, default=None)

   :param str key: keyname

   Get attribute `key` of `wrapped` XML node, or `default` if
   key doesn't exist.

.. method:: GenericWrapper.set_attr(key, value)

   :param str key: keyname
   :param str value: value

   Set attribute `key` of the `wrapped` XML node to value.

.. method:: GenericWrapper.append(child)

   :param GenericWrapper child: append `wrapped` XML node

   Append `child` as last child into the `wrapped` XML node.

.. method:: GenericWrapper.insert_before(target, child)

   :param GenericWrapper target: target node
   :param GenericWrapper child: new node

   Insert `child` before the target node `target`.

.. method:: GenericWrapper.remove(child)

   :param GenericWrapper child: wrapped XML node

   Remove `child` from node.

.. method:: GenericWrapper.clear()

   Clear node content (text, tail, attributes) and remove all children.

.. method:: GenericWrapper.plaintext()

   Returns the plaintext representation of the node.