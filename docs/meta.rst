.. _meta module:

meta module
===========

In the `meta` module contains all classes to access the documents
meta data, keywords and user defined tags.

- `Meta` class gives you access to the simple meta data
- `Keywords` class gives you access to the document keywords
- `Usertags` class gives you access to the user defined tags

Every ODF document class has an attribute called `meta` which is an instance
of `Meta` class.

.. _Meta class:

Meta class
----------

- you always get/set strings
- also for date and time values

You got access to the documents metatags by the [ ] operator::

    # get values
    value = document.meta['generator']
    # set values
    document.meta['description'] = "This is a text document."

At this time the supported metatags are:

================ ============================================================
Metatag          Description
================ ============================================================
generator        application or tool that was used to create or last modify
                 the XML document.
title            title of the document
description      brief description of the document
subject          subject of the document
initial-creator  name of the person who created the document initially
creator          name of the person who last modified the document
creation-date    date and time when the document was created initially
                 ISO format  YYYY-MM-DDThh:mm:ss

date             date and time when the document was last modified
                 (ISO format)
editing-cycles   number of editing cycles the document has been through.
                 The value of this element is incremented every time
                 the document is saved.
language         the document language like ``'en-US'`` or ``'de-AT'``
================ ============================================================

Attributes
~~~~~~~~~~

.. attribute:: keywords

   Attribute of the `Meta` class, gives you access to the documents
   keywords by the :ref:`Keywords class`.

.. attribute:: usertags

   Attribute of the `Meta` class, gives you access to the documents
   user defined tags by the :ref:`Usertags class`.

.. _Keywords class:

Keywords class
--------------

The `Keywords` class manages the `<meta:keyword>` elements.

Methods
~~~~~~~

.. method:: add(keyword)

   Add `keyword` to the document meta data.

.. method:: remove(keyword)

   remove `keyword` from the document meta data.

.. method:: __iter__()

   Iterate over all `keywords`::

       for keyword in document.meta.keywords:
          pass # or do something

.. method:: __contains__(keyword)

   `True` if `keyword` is in the meta data else `False`.

   This method is used by the **in** operator::

       if 'text' in document.meta.keywords:
           pass # or do something

Usertags class
--------------

.. _Usertags class:

The `Usertags` class manages the `<meta:user-defined>` elements.

Methods
~~~~~~~

.. method:: set(name, value, value_type=None)

   Set the usertag `name` the `value` and the type to `value_type`.

.. method:: __setitem__(name, value)

   Set usertag `name` to `value`, type is ``'string'``.

.. method:: __getitem__(name)

   Get usertag `name`.

.. method:: __delitem__(name)

   Delete usertag `name`.

   usage::

       document.meta.usertags['mytag'] = 'text'
       value = document.meta.usertags['mytag']
       del document.meta.usertags['mytag']

.. method:: __iter__()

   Iterate over all `usertags`, returns 2-tuple (tagname, tagvalue)::

       for name, value in document.meta.usertags:
          pass # or do something

.. method:: __contains__(name)

   `True` if the document has a usertag `name` else `False`.

   This method is used by the **in** operator::

       if 'mytag' in document.meta.usertags:
           pass # or do something
