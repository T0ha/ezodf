How-Tos
=======

.. _howtos_general:

General Document Management
---------------------------

**How do I open an ODF document?**

see :ref:`opendoc`

**How do I create a new ODF document?**

see :ref:`newdoc`

**Where is the document content?**

All ODF objects, like :class:`~text.Paragraph` or :class:`~text.Heading`, resides
in the :attr:`~document.PackagedDocument.body` attribute of the document object.
All data management function are method calls of this object.

**How do I append/insert ODF objects to a document?**

Use the :attr:`~document.PackagedDocument.body` attribute of the document object::

    p1 = doc.body.append(Paragraph('text1'))
    p2 = doc.body.insert_before(p1, Paragraph('text2'))

    # insert object at 'position'
    doc.body.insert(0, Paragraph('New first paragraph.'))

**How do I get ODF objects from a document?**

1. You can iterate over all objects at the top-level of the body object::

       for obj in doc.body:
           pass
           # do something

2. If you know the position of the object, you can access the object by the
   subscript operator::

       p1 = doc.body[0] # first object of the document
       count = len(doc.body) # get count of the top-level objects

3. If you look for an specific object type, use the :func:`~base.GenericWrapper.filter`
   method to search for all child objects selected by the :attr:`~base.GenericWrapper.kind`
   attribute::

      # kind is the name of the element wrapper class
      paragraphs = doc.body.filter(kind='Paragraph')

   or use the :func:`~base.GenericWrapper.findall` method to find all children
   by their XML tag (in Clark Notation, see :func:`~xmlns.CN` function), this is
   a wrapper for the :func:`lxml.Element.findall` method (see `lxml API Reference`_)::

      paragraphs = doc.body.findall(CN('text:p'))

**How do I get the position of an object?**

   Use the :func:`~base.GenericWrapper.index` method::

      pos = doc.body.index(p1)

      # get the previous object of p1
      prev = doc.body[pos-1]

.. _howtos_text:

Text Documents
--------------

**How to insert a page break?**

Add :class:`~whitespaces.SoftPageBreak` object to heading or paragraph::

   p = doc.body.append(Paragraph("some text"))
   p.append(SoftPageBreak())

.. _howtos_spreadsheet:

Spreadsheet Documents
---------------------

.. _howtos_presentation:

Presentation Documents
----------------------

.. _howtos_drawing:

Drawing Documents
-----------------

.. _howtos_style:

Style Management
----------------


.. _lxml API Reference: http://codespeak.net/lxml/api/index.html