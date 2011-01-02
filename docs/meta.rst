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

   Attribute of the `Meta` class, got you access to the documents
   keywords by the :ref:`Keywords class`.

.. attribute:: usertags

   Attribute of the `Meta` class, got you access to the documents
   user defined tags by the :ref:`Keywords class`.

.. _Keywords class:

Keywords class
--------------

.. _Usertags class:

Usertags class
--------------

