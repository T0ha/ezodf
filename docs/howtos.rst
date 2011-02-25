How-Tos
=======

.. _howtos_general:

General Document Management
---------------------------

**How to open an ODF document?**

::

   doc = ezodf.opendoc(filename)

see :ref:`opendoc`

**How to open an ODF document from a file-like object?**

`stream` is a file-like object, opened in binary mode::

    buffer = stream.read()
    doc = ezodf.open(buffer)

**How to create a new ODF document?**

::

   doc = ezodf.newdoc(doctype, filename)

see :ref:`newdoc`

**How to save the document?**

::

   # save with filename given at opendoc() or newdoc()
   doc.save()
   # save with a new name
   doc.saveas(filename, backup=True)

**How to manage the document without filesystem access?**

You can also get the document zip-file as `bytes`.

::

   # get content as bytes
   buffer = doc.tobytes()
   # and reopen the document
   doc = ezodf.opendoc(buffer)
   # or use it as template for a new document
   doc = ezodf.newdoc(template=buffer)

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

Use the :func:`ezodf.ezlist` function, creates an unnumbered list as default, use
the `style_name` parameter to use a different list-style::

   ulist = ezodf.ezlist(['Point 1', 'Point 2', 'Point 3'])
   doc.body.append(ulist)

.. _howtos_spreadsheet:

Spreadsheet Documents
---------------------

**Prelude**

::

   from ezodf import newdoc, opendoc, Sheet

   # create a new spreadsheet document
   doc = newdoc(doctype='ods', filename='spreadsheet.ods')
   # or open an existing spreadsheet document
   doc = opendoc('spreadsheet.ods')

.. _howtos_sheets:

Managing Sheets
~~~~~~~~~~~~~~~

**How to add a new sheet?**

Sheets are :class:`Sheet` objects and resides in the :attr:`sheets` attribute
of the spreadsheet-document::

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

**How to move a sheet?**

To move a sheet in front of another sheet just insert the moving sheet::

   sheet1 = doc.sheets[0]
   sheet2 = doc.sheets[1]
   # move sheet2 in front of sheet1
   doc.sheets.insert(0, sheet2)

You can insert a sheet as often you want, there is alway just one instance of
the sheet in the document. You can also move a sheet to another document, but
referenced styles will not be copied automatically::

   sheet = doc1.sheets[0]
   doc2.sheets.append(sheet)

**How to copy a sheet?**

Make a copy of the sheet and insert or append the copy::

   duplicate = sheet.copy(newname='CopyOf'+sheet.name)
   doc.sheets += duplicate

**How to get all sheet names?**

::

   names = doc.sheets.names() # returns a generator object

.. _howtos_sheet_geometry:

Managing Sheet Geometry
~~~~~~~~~~~~~~~~~~~~~~~

**Prelude**

::

   sheet = doc.sheets[0]

**How to get sheet metrics?**

::

   count_of_rows = sheet.nrows()
   count_of_colmns = sheet.ncols()
   name = sheet.name

**How to insert/append new rows/columns?**

.. warning::

   insert operations break cell references in formulas

Appending new empty rows/columns::

   sheet.append_rows(2)
   sheet.append_columns(3)

Inserting new empty rows/columns at position `index`::

   sheet.insert_rows(index=3, count=2)
   sheet.insert_columns(index=3, count=2)

**How to delete rows/columns?**

.. warning::

    delete operations break cell references in formulas

::

   sheet.delete_rows(index=3, count=2)
   sheet.delete_columns(index=3, count=2)

.. _howtos_sheet_content:

Managing Sheet Content
~~~~~~~~~~~~~~~~~~~~~~

**Prelude**

::

   sheet = doc.sheets[0]

**How to reference cells?**

Cells are referenced by a (row, column) tuple or by classsic spreadsheet
references like ``'A1'`` for cell (0, 0), letters stands for
columns, numbers stands for rows, and as you see the row/column index is zero-based,
where classic references start with row = ``'1'`` and column = ``'A'``.

**How to get the cell content?**

The cell content is manged by the :class:`Cell` class::

   cell = sheet['A1']
   value = cell.value
   value_type = cell.value_type

   value = sheet['A1'].value

- for ``'string'``, ``'date'`` and ``'time'``: you get `str` objects
- for ``'float'``, ``'precentage'`` and ``'currency'``: you get `float` objects
- for ``'boolean'``: you get `bool` objects

**How to modify cell content?**

::

   # for str, float and bolean values, you can ignore the value_type
   sheet['A1'].set_value('a string value')

   # setting a currency
   sheet['A1'].set_value(100, currency='EUR') # is equal to
   sheet['A1'].set_value(100, 'currency', 'EUR')

   # setting a date
   sheet['A1'].set_value('2011-02-05', 'date')
   sheet['A1'].set_value('2011-02-05T09:24:00', 'date') # /w time

   # setting a time-period 1:10:05
   sheet['A1'].set_value('PT01H10M05,0000S', 'time')

to convert date/timeperiod values see :class:`TimeParser` class. Here just a few
examples::

   from ezodf.timeparser import TimeParser

   date_object = TimeParser.parse('2011-02-05')
   datetime_object = TimeParser.parse('2011-02-05T09:24:00')
   timedelta_object = TimeParser.parse('PT01H10M05,0000S')

   # timedelta to str: 'PThhHmmMss,ffffS'
   time_period_str = str(TimeParser(timedelta_object))

**How to get rows/columns?**

::

   row0 = sheet.row(0) # as list of Cell() objects
   col0 = sheet.column(0) # as list of Cell() objects

**How to iterate over rows/columns?**

::

   for row in sheet.rows():
      print row # row is a list of Cell() objects

   for column in sheet.columns():
      print column # column is a list of Cell() objects

**How about spreadsheet calculations?**

**ezodf** has no calculation engine included, you can get/set formulas as strings,
nothing more. So display form and cell value will not be updated if content is
changed, and inserting/deleting rows/columns will also break cell references in
formulas.

.. _howtos_presentation:

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

- style an object with `LibreOffice` or `OpenOffice`
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