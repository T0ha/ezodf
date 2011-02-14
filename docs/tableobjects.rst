.. _tableobjects:

Table Objects
=============

Sheets Class
------------

.. class:: Sheets

   The :class:`Sheets` manages all :class:`Table` objects in
   spreadsheet-documents. (`sheet` is a synonym for `table`)

.. warning::

   Don't create instances of this class by yourself, every spreadsheet-document
   has a :attr:`sheets` attribute.

Methods
~~~~~~~

.. method:: Sheets.__len__()

   Get count of sheets.

.. method:: Sheets.__iter__()

   Iterate over all :class:`Table` objects.

.. method:: Sheets.__getitem__(key)

   Get sheet by `key`, `key` is either the numerical index of the sheet or
   the name of the sheet.

.. method:: Sheets.__setitem__(key, sheet)

   Replace sheet `key` by `sheet`, `key` is either the numerical index of the
   sheet or the name of the sheet.

.. method:: Sheets.__delitem__(key)

   Delete sheet by `key`, `key` is either the numerical index of the sheet or
   the name of the sheet.

.. method:: Sheets.__iadd__(sheet)

   ``+=`` operator, alias for :meth:`~Sheets.append`.

.. method:: Sheets.append(sheet)

   Append `sheet` as last sheet of spreadsheet-document.

.. method:: Sheets.index(sheet)

   Get index of `sheet`.

.. method:: Sheets.insert(index, sheet)

   Insert `sheet` at position `index`.

.. method:: Sheets.names()

   Get list of sheet names.

Table Class
-----------

.. class:: Table(name="NEWTABLE", size=(10, 10), xmlnode=None)

   The :class:`Table` object represents a fixed sized table with `size[0]` rows
   and `size[1]` columns. Every cell contains a :class:`Cell` object, even empty
   cells (`value` and `value_type` of empty cells are `None`).

   Reference cells by (row, col) tuples or by classic spreadsheet cell references
   like ``'A1'``. The letters represent the column (``'A'`` = column(0), ``'B'``
   = column(1), ...), the numbers represent the row (``'1'`` = row(0), ``'2'``
   = row(1), ...).

Attributes
~~~~~~~~~~

.. attribute:: Table.name (read/write)

   Specifies the name of the table, should be unique, and can contain spaces.

.. attribute:: Table.style_name (read/write)

   References a table style.

.. attribute:: Table.protected (read/write)

   The :attr:`~Table.protected` attribute specifies whether or not a table is
   protected from editing. If a table is protected, all of the table elements
   and the cell elements with a :attr:`~Cell.protected` attribute set to `True`
   are protected.

Methods
~~~~~~~

.. method:: Table.__getitem__(key)

   Get cell by `key` as :class:`Cell` object, `key` is either a
   (`row, col`) tuple or a classic spreadsheet reference like ``'A1''``.

.. method:: Table.__setitem__(key, cell)

   Set cell referenced by `key` to `cell`, `cell` has to be a :class:`Cell`
   object and `key` is either a (`row, col`) tuple or a classic spreadsheet
   reference like ``'A1''``.

.. method:: Table.ncols()

   Get count of table columns.

.. method:: Table.nrows()

   Get count of table rows.

.. method:: Table.reset(size=(10, 10))

   Delete table content and set new table metrics.

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

   Insert `count` empty rows at `index`. **CAUTION:** This operation breaks cell
   references in formulas

.. method:: Table.delete_rows(index, count=1)

   Delete `count` rows at `index`. **CAUTION:** This operation breaks cell
   references in formulas

.. method:: Table.append_columns(count=1)

   Append `count` empty columns.

.. method:: Table.insert_columns(index, count=1)

   Insert `count` empty columns at `index`. **CAUTION:** This operation breaks
   cell references in formulas

.. method:: Table.delete_columns(index, count=1)

   Delete `count` columns at `index`. **CAUTION:** This operation breaks cell
   references in formulas

.. method:: Table.set_cell_span(pos, size)

   Set cell span for cell at position `pos` to `size`, `pos` can be a
   (row, column) tuple or a reference string, `size` has to be a (nrows, ncols)
   tuple, where nrows and ncols are >= 1. Spanning is not possible if the
   spanning area contains other spanning cells.

   The cell span value is an attribute of the :class:`Cell` class. To request
   the span value use::

       if table['A1'].span == (3, 2):
           print("cell 'A1' spans over three rows and two columns")

.. method:: Table.remove_cell_span(pos)

   Removes spanning for cell at position `pos`, `pos` can be a
   (row, column) tuple or a reference string.

Sheet Class
-----------

.. class:: Sheet

   Alias for :class:`Table` class.

Cell Class
----------

.. class:: Cell(value=None, value_type=None, currency=None, style_name=None, xmlnode=None)

   Creates a new cell object. If `value_type` is None, the type will be determined
   by the type of `value`. `value` and `value_type` of empty cells are `None`.

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

examples for setting table values::

    # create new cell as float
    table['A1'] = Cell(100.)
    # or modify existing cell (preserves existing properties)
    table['A1'].set_value(100.)
    # set as currency
    table['B1'].set_value(100, currency='EUR')
    # set as string
    table['C1'].set_value("Text")
    # append text to string-cells
    table['C1'].append_text("\nLine 2")
    # set as date
    table['D1'].set_value("2011-02-05", 'date')

example for getting cell values::

    cell = Cell(3.141592)
    pi = cell.value

Attributes
~~~~~~~~~~

.. attribute:: Cell.value (read)

   Get converted cell values, numerical values as `float`, boolean values as
   `bool` and all others as `str`.

.. attribute:: Cell.value_type (read)

.. attribute:: Cell.currency (read)

   Get currency as `string`, if :attr:`Cell.value_type` is ``'currency'``
   else `None`.

.. attribute:: Cell.style_name (read/write)

   References a table-cell style.

.. attribute:: Cell.formula (read/write)

   Formulas allow calculations to be performed within table cells. Typically,
   the formula itself begins with an equal (=) sign and can include the following
   components:

   - Numbers
   - Text
   - Named ranges
   - Operators
   - Logical operators
   - Function calls
   - Addresses of cells that contain numbers

.. attribute:: Cell.content_validation_name (read/write)

.. attribute:: Cell.protected (read/write)

   Protects the table cell. Users can not edit the content of a cell
   that is marked as protected. This attribute is not related to the
   :attr:`Table.protected` attribute for table elements.

.. attribute:: Cell.span (read)

   Get cell spanning as (row, col) tuple.

   Specify the number of rows and columns that a cell spans.
   When a cell covers another cell because of a column or row span value
   greater than one, the :attr:`~Cell.covered` attribute of the covered
   cell is `True`.

.. attribute:: Cell.covered (read)

   `True` if cell is covered by other cells.

.. attribute:: Cell.display_form (read/write)

   Display form of cell as `str`, set by other programs like LibreOffice or
   OpenOffice. **ezodf** does not set the display form.

Methods
~~~~~~~

.. method:: Cell.set_value(value, value_type=None, currency=None)

   Set new cell velues.

.. method:: Cell.plaintext()

   Get the plain text representation as `str`.

.. method:: Cell.append_text()

   Append text to cells of type ``'string'``.

TableRow Class
--------------

.. class:: TableRow

Attributes
~~~~~~~~~~

.. attribute:: TableRow.style_name (read/write)

   References a table-row style.

.. attribute:: TableRow.visibility (read/write)

   Specifies whether the row is ``'visible'``, ``'filtered'``, or ``'collapsed'``.

   Filtered and collapsed rows are not visible. Filtered rows are invisible,
   because a filter is applied to the table that does not select the table
   row. Collapsed rows have been made invisible by user directly.

.. attribute:: TableRow.default_cell_style_name (read/write)

   References the default table-cell style.

TableColumn Class
-----------------

Attributes
~~~~~~~~~~

.. class:: TableColumn

.. attribute:: TableColumn.style_name (read/write)

   References a table-column style.

.. attribute:: TableColumn.visibility (read/write)

   Specifies whether the row is ``'visible'``, ``'filtered'``, or ``'collapsed'``.

   Filtered and collapsed columns are not visible. Filtered columns are invisible,
   because a filter is applied to the table that does not select the table
   column. Collapsed columns have been made invisible by user directly.

.. attribute:: TableColumn.default_cell_style_name (read/write)

   References the default table-cell style.
