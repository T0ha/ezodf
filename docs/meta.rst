Meta Data Management
====================

.. module:: meta

In the `meta` module contains all classes to access the documents
meta data, keywords and user defined tags.

- :class:`Meta` class gives you access to the simple meta data
- :class:`Keywords` class gives you access to the document keywords
- :class:`Usertags` class gives you access to the user defined tags
- :class:`Statistic` class gives you access to the document statistics

Every ODF document class has an attribute called :attr:`~document.PackagedDocument.meta`
which is an instance of :class:`Meta` class.

Meta Class
----------

.. class:: Meta()

.. warning::

   Don't create instances of this class by yourself.

You always get/set strings, also for date and time values.

Methods
~~~~~~~

.. method:: Meta.__setitem__(key, value)

   Set metatag `name` to `value`.

.. method:: Meta.__getitem__(name)

   Get metatag `name`.

You got access to the documents metatags by the `subscript` operator::

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

.. method:: Meta.clear()

   Delete all metatags, keywords, user-defined tags and statistics.

Attributes
~~~~~~~~~~

.. attribute:: Meta.keywords

   The :attr:`~Meta.keywords` attribute gives you access to the documents
   keywords by the :class:`Keywords` class.

.. attribute:: Meta.usertags

   The :attr:`~Meta.usertags` attribute gives you access to the documents
   user defined tags by the :class:`Usertags` class.

.. attribute:: Meta.count

   The :attr:`~Meta.count` attribute  gives you access to the documents
   statistics by the :class:`Statistic` class.

Keywords Class
--------------

.. class:: Keywords

   The :class:`Keywords` class manages the `<meta:keyword>` elements.

.. warning::

   Don't create instances of this class by yourself.

Methods
~~~~~~~

.. method:: Keywords.add(keyword)

   Add `keyword` to the document meta data.

.. method:: Keywords.remove(keyword)

   remove `keyword` from the document meta data.

.. method:: Keywords.__iter__()

   Iterate over all `keywords`::

       for keyword in document.meta.keywords:
          pass # or do something

.. method:: Keywords.__contains__(keyword)

   `True` if `keyword` is in the meta data else `False`.

   This method is used by the **in** operator::

       if 'text' in document.meta.keywords:
           pass # or do something

.. method:: Keywords.clear()

   Delete all keywords.

Usertags Class
--------------

.. class:: Usertags

   The :class:`Usertags` class manages the `<meta:user-defined>` elements.

.. warning::

   Don't create instances of this class by yourself.

Methods
~~~~~~~

.. method:: Usertags.set(name, value, value_type=None)

   Set the usertag `name` the `value` and the type to `value_type`. The
   allowed meta types are ``'float'``, ``'date'``, ``'time'``, ``'boolean'``
   and ``'string'``.

.. method:: Usertags.__setitem__(name, value)

   Set usertag `name` to `value`, type is ``'string'``.

.. method:: Usertags.__getitem__(name)

   Get usertag `name`.

.. method:: Usertags.__delitem__(name)

   Delete usertag `name`.

   usage::

       document.meta.usertags['mytag'] = 'text'
       value = document.meta.usertags['mytag']
       del document.meta.usertags['mytag']

.. method:: Usertags.typeof(name)

   Get type of user defined tag `name`. The allowed meta types are ``'float'``,
   ``'date'``, ``'time'``, ``'boolean'`` and ``'string'``.

.. method:: Usertags.__contains__(name)

   `True` if the document has a usertag `name` else `False`.

   This method is used by the **in** operator::

       if 'mytag' in document.meta.usertags:
           pass # or do something

.. method:: Usertags.__iter__()

   Iterate over all `usertags`, returns 2-tuple (tagname, tagvalue)::

       for name, value in document.meta.usertags:
          pass # or do something

       # create a dict of user defined tags
       d = dict(document.meta.usertags)

.. method:: Usertags.update(d)

   Set user defined tags from dict `d`.

.. method:: Usertags.clear()

   Delete all user defined tags.


Statistic Class
---------------

.. class:: Statistic

   The :class:`Statistic` class manages the `<meta:document-statistic>` element.

.. warning::

   Don't create instances of this class by yourself.

Methods
~~~~~~~

.. method:: Statistic.__getitem__(key)

   Get count of statistic element `key` as `int`, if `key` is not defined
   for the document the result is ``0``.

.. method:: Statistic.__setitem__(key, value)

   Set count of statistic element `key` to `value`.

   usage::

      if document.meta.count['page'] > 3:
          pass # or do something
      # or set values
      document.meta.count['character'] = 4711

.. method:: Statistic.__iter__()

   Iterate over all statistics, returns 2-tuple (element, value).

   create a dict of all statistic values::

      d = dict(document.meta.count)

.. method:: Statistic.update(d)

   Set statistics from dict `d`.

.. method:: Statistic.clear()

   Clear all statistics.

======================== ====================================================
Element                  Description
======================== ====================================================
page                     Number of pages in a word processing document. This
                         must be greater than zero. This attribute is not
                         used in spreadsheets. The page-count for a
                         spreadsheet is a calculated value that tells how
                         many sheets have filled cells on them, and this can
                         be zero for a totally empty spreadsheet.
table                    Number of tables in a word processing document, or
                         number of sheets in a spreadsheet document.
draw                     Apparently unused in OpenOffice.org2.0
image                    Number of images in a word processing document.
object                   Number of objects in a document. This attribute is
                         used in drawing and presentation documents, but it
                         does not bear any simple relationship to the number
                         of items you see on the screen.
ole-object               Apparently unused in OpenOffice.org2.0
paragraph                Number of paragraphs in a word processing document.
word                     Number of words in a word processing document.
character                Number of characters in a word processing document.
row                      Apparently unused in OpenOffice.org2.0
frame                    unknown
sentence                 Number of sentences in a word processing document.
syllable                 Number of syllables in a word processing document.
non-whitespace-character Number of non-whitespace-characters in a word
                         processing document.
cell                     none empty cells in a spreadsheet document.
======================== ====================================================

Table from the online book `OASIS OpenDocument Essentials`_.

.. _OASIS OpenDocument Essentials: http://books.evc-cit.info/