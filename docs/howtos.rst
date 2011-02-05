How-Tos
=======

.. _howtos_general:

General Document Management
---------------------------

**How to open an ODF document?**

::

   doc = ezodf.opendoc(filename)

see :ref:`opendoc`

**How to create a new ODF document?**

::

   doc = ezodf.newdoc(doctype, filename)

see :ref:`newdoc`

**Where is the document content?**

All ODF objects, like :class:`~text.Paragraph` or :class:`~text.Heading`, resides
in the :attr:`~document.PackagedDocument.body` attribute of the document object.
All data management function are method calls of this object.

**How to append/insert ODF objects to a document?**

Use the :attr:`~document.PackagedDocument.body` attribute of the document object::

    p1 = doc.body.append(Paragraph('text1'))
    p2 = doc.body.insert_before(p1, Paragraph('text2'))

    # insert object at 'position'
    doc.body.insert(0, Paragraph('New first paragraph.'))

**How to get ODF objects from a document?**

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

**How to get the position of an object?**

::

   pos = doc.body.index(p1)

   # get the previous object of p1
   prev = doc.body[pos-1]

.. _howtos_text:

Text Documents
--------------

**Prelude**

::

   # create a new text document
   doc = ezodf.newdoc(doctype='odt', filename='text.odt')
   # or open an existing text document
   doc = ezodf.opendoc('text.odt')

**How to add a heading?**

Add :class:`~text.Heading` object to the :attr:`~document.PackagedDocument.body`
attribute of the document::

   doc.body.append(Heading('A text paragraph.')

**How to add a text paragraph?**

Add :class:`~text.Paragraph` object to the :attr:`~document.PackagedDocument.body`
attribute of the document::

   doc.body.append(Paragraph('A text paragraph.')

**How to insert a page break?**

Add :class:`~whitespaces.SoftPageBreak` object to heading or paragraph::

   p = doc.body.append(Paragraph("some text"))
   p.append(SoftPageBreak())

**How to create a simple list?**

Use the :func:`ezodf.ezlist` function, creates unnumbered lists as default, use
the `style_name` parameter to assign an new list-style::

   ulist = ezodf.ezlist(['Point 1', 'Point 2', 'Point 3'])
   doc.body.append(ulist)

.. _howtos_spreadsheet:

Spreadsheet Documents
---------------------

**Prelude**

::

   # create a new spreadsheet document
   doc = ezodf.newdoc(doctype='ods', filename='spreadsheet.ods')
   # or open an existing spreadsheet document
   doc = ezodf.opendoc('spreadsheet.ods')

.. _howtos_sheets:

Managing Sheets
~~~~~~~~~~~~~~~

.. _howtos_presentation:

**How to add a new sheet?**

Sheets are :class:`Sheet` objects and resides in the :attr:`sheets` attribute
of the document::

   # append new sheets at the end of the document
   doc.sheets += Sheet('ANewSheet')
   doc.sheets.append('AnotherSheet')
   # or insert the new sheet at an arbitary position
   doc.sheet.insert(1, Sheet('AsSecondSheet'))

**How to get sheets from document?**

You can get sheets by `index` or by `name`::

   # get first sheet
   sheet = doc.sheets[0]
   # get last sheet
   sheet = doc.sheets[-1]
   # get sheet by name
   sheet = doc.sheets['ANewSheet']

   # iterate over sheets
   for sheet in doc.sheets:
      print sheet.name

**How to get position of a sheet?**

::

   index = doc.sheets.index(sheet)

   # get count of sheets
   count = len(doc.sheets)

**How to delete a sheet?**

::

   del doc.sheets[0]

**How to replace a sheet?**

::

   doc.sheets[0] = Sheet('ReplaceFirstSheet')

.. _howtos_sheet:

Managing Sheet Content
~~~~~~~~~~~~~~~~~~~~~~

Presentation Documents
----------------------

.. _howtos_drawing:

Drawing Documents
-----------------

.. _howtos_style:

Style Management
----------------

**How to use styles, while style-management is not implemented?**

In existing documents, you can use the included styles, you find the needed
``style:name`` attributes in `styles.xml` or `content.xml`, search for
``<style:style style:name="...">`` elements.

For new documents you can copy&paste styles from other documents:

- style an object with LibreOffice or OpenOffice
- save & unzip document
- in content.xml: search styled object, search the associated automatic style,
  search for ``<style:style style:name="...">`` elements
- copy style-element (``<style:style> ... </style:style>``) to clipboard

rest follows in Python, use a meaningful and unique ``style:name`` attribute::

   doc.inject_style("""... insert clipboard content ...""")

or use a document including styles as template: newdoc('odt', template='template.odt')

to apply the style, just use the name associated by the `style:name` attribute::

   doc.append(Paragraph("some text", style_name='...'))


.. _lxml API Reference: http://codespeak.net/lxml/api/index.html