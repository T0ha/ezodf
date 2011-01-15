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

   Register `cls` for wrapping mechanism.
   Can be used as class decorator.
   `cls` has to have a :attr:`cls.TAG` attribute in Clark-Notation which
   determines the XML element to wrap, and `cls` has to accept the keyword
   attribute `xmlnode` on the `__init__()` constructor, which is the
   :class:`lxml.Element` object to wrap. (see :class:`~base.GenericWrapper`)

.. seealso:: :class:`base.GenericWrapper`

.. function:: wrap(element)

   Wrap element into a wrapper object, where element is an
   :class:`lxml.Element` object. Returns a :class:`~base.GenericWrapper` object,
   if no class is registered for `element`.