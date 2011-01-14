.. module:: xmlns

XML Namespace Helper Tools
==========================

Functions
---------

.. function:: CN(tag)

   Convert Prefix-Notation to Clark-Notation. All OpenDocument V1.1
   Namespaces are respected::

     CN('text:p') == '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'

.. function:: register_class(cls)

   Register `cls` for wrapping mechanism. Can be used as class decorator.
   `cls` has to have a :attr:`cls.TAG` attribute in Clark-Notation which
   determines the XML element to wrap, and `cls` has to accept the keyword attribute
   `xmlnode` which is the :class:`lxml.Element` object to wrap.

.. seealso:: :class:`base.GenericWrapper`

.. function:: wrap(element)

   Wrap element into a Python wrapper object, where element is an
   :class:`lxml.Element` object. Returns the :class:`base.GenericWrapper` if
   no other python class is registered for `element`.