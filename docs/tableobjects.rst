.. _tableobjects:

Table Objects
=============

Sheets Class
------------

.. class:: Sheets(xmlbody)

   The :class:`Sheets` manages all :class:`Table` objects in an
   spreadsheet-document. (`sheet` is a synonym for `table`)

.. warning::

   Don't create instances of this class by yourself, every spreadsheet-document
   has a :attr:`sheets` attribute.

Methods
~~~~~~~

.. method:: Sheets.__len__()

   Get count of sheets. (use `len(sheets)`)

.. method:: Sheets.__iter__()

   Iterate over all :class:`Table` objects. (use `iter(sheets)`)

.. method:: Sheets.__getitem__(key)

.. method:: Sheets.__setitem__(key, value)

.. method:: Sheets.__delitem__(key)

.. method:: Sheets.__iadd__(sheet)

.. method:: Sheets.append(sheet)

.. method:: Sheets.index(sheet)

.. method:: Sheets.insert(index, sheet)

.. method:: Sheets.names()

Table Class
-----------

.. class:: Table(name="NEWTABLE", size=(10, 10), xmlnode=None)

Attributes
~~~~~~~~~~

.. attribute:: Table.name (read/write)

.. attribute:: Table.style_name (read/write)

.. attribute:: Table.protected (read/write)

.. attribute:: Table.print (read/write)

Methods
~~~~~~~

.. method:: Table.__getitem__(key)

.. method:: Table.__setitem__(key, value)

.. method:: Table.ncols()

   Get count of table columns.

.. method:: Table.nrows()

   Get count of table rows.

.. method:: Table.reset(size=(10, 10))

   Delete table-content and set new table metrics.

.. method:: Table.row(index)

   Get cells of row `index` as list of :class:`Cell` objects.

.. method:: Table.rows(index)

   Iterate over rows, where every row is a list of :class:`Cell` objects.

.. method:: Table.col(index)

   Get cells of column `index` as list of :class:`Cell` objects.

.. method:: Table.columns(index)

   Iterate over columns, where every column is a list of :class:`Cell` objects.

.. method:: Table.row_info(index)

   Get row-info of row `index` as :class:`TableRow` object.

.. method:: Table.column_info(index)

   Get column-info of column `index` as :class:`TableColumn` object.

.. method:: Table.append_rows(count=1)

   Append `count` empty rows.

.. method:: Table.insert_rows(index, count=1)

   Insert `count` empty rows at `index`. **CAUTION:** This operations breaks cell
   references in formulas

.. method:: Table.delete_rows(index, count=1)

   Delete `count` rows at `index`. **CAUTION:** This operations breaks cell
   references in formulas

.. method:: Table.append_columns(count=1)

   Append `count` empty columns.

.. method:: Table.insert_columns(index, count=1)

   Insert `count` empty columns at `index`. **CAUTION:** This operations breaks
   cell references in formulas

.. method:: Table.delete_columns(index, count=1)

   Delete `count` columns at `index`. **CAUTION:** This operations breaks cell
   references in formulas

Sheet Class
-----------

.. class:: Sheet

   Alias for :class:`Table` class.

Cell Class
----------

.. class:: Cell(value=None, value_type=None, currency=None, style_name=None, xmlnode=None)

   Creates a new cell object. If `value_type` is None, the type will be determined
   by the type of `value`.

================ ===============================================================
Value Type       Description
================ ===============================================================
``'string'``     Text content (python strings)
``'float'``      Floating point numbers (python float)
``'percentage'`` Floating point numbers, where 1.0 = 100% (python float)
``'currency'``   Floating point numbers (python float)
``'boolean'``    `True` or `False` (python bool)
``'date'``       date value as string, form: ``'yyyy-mm-dd'`` or
                 ``'yyyy-mm-ddThh:mm:ss'``
``'time'``       time period as string, form: ``'PThhHmmMss,ffffS``'
================ ===============================================================

Automatic typing:

===================== =======================
Python type of Value  value_type of cell
===================== =======================
str                   ``'string'``
float/int             ``'float'``
bool                  ``'boolean'``
===================== =======================

Attributes
~~~~~~~~~~

.. attribute:: Cell.value (read)

.. attribute:: Cell.value_type (read)

.. attribute:: Cell.currency (read)

.. attribute:: Cell.style_name (read/write)

.. attribute:: Cell.formula (read/write)

.. attribute:: Cell.content_validation_name (read/write)

.. attribute:: Cell.protected (read/write)

.. attribute:: Cell.span (read)

.. attribute:: Cell.covered (read)

.. attribute:: Cell.display_form (read/write)

Methods
~~~~~~~

.. method:: Cell.set_value(value, value_type=None, currency=None)

.. method:: Cell.plaintext()

.. method:: Cell.append_text()


TableRow Class
--------------

.. class:: TableRow

Attributes
~~~~~~~~~~

.. attribute:: TableRow.style_name (read/write)

.. attribute:: TableRow.visibility (read/write)

.. attribute:: TableRow.default_cell_style_name (read/write)

TableColumn Class
-----------------

.. class:: TableColumn

.. attribute:: TableColumn.style_name (read/write)

.. attribute:: TableColumn.visibility (read/write)

.. attribute:: TableColumn.default_cell_style_name (read/write)
