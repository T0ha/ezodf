.. module:: spreadsheet

Spreadsheet Document
====================

Definition: https://secure.wikimedia.org/wikipedia/en/wiki/Spreadsheet

A spreadsheet is a computer application that simulates a paper, accounting
worksheet. It displays multiple cells usually in a two-dimensional matrix or
grid consisting of rows and columns. Each cell contains alphanumeric text, numeric
values or formulas. A formula defines how the content of that cell is to be
calculated from the contents of any other cell (or combination of cells) each
time any cell is updated (**ezodf** has no calculation-engine included!).
A pseudo third dimension to the matrix is sometimes applied as another sheet,
of two-dimensional data.

Document Management
-------------------

You can create new spreadsheet-documents or open existing
documents to modify their content.

create a new document::

    spreadsheet = ezodf.newdoc(doctype="ods", filename="spreadsheet.ods")

or open an existing document::

    spreadsheet = ezodf.opendoc("spreadsheet.ods")

.. seealso:: :ref:`opendoc` and  :ref:`newdoc`

Sheet Management
----------------

A spreadsheet document should contain at least one :class:`Table` object. In the
context of a spreadsheet document I use **sheet** as synonym for the :class:`Table`
class, which manages the sheet content. These sheets are accessible by the
:attr:`sheets` attribute (:class:`Sheets` object) of the spreadsheet document.
All sheets names should be unique, and can contain spaces.

Supported operations:

* append/insert new sheets
* replace existing sheet
* delete existing sheets

examples::

    sheets = spreadsheet.sheets
    # append a new sheet
    sheets += ezodf.Table('Sheet1')
    # or
    sheets.append(ezodf.Table('Sheet2'))
    # get a sheet by index
    sheet = sheets[0]
    # get a sheet by name
    sheet = sheets['Sheet1']
    # iterate over all sheets
    for sheet in sheets:
        print sheet.name
    # replace an existing sheet
    sheets['Sheet2'] = ezodf.Table('Sheet3')
    # insert a sheet at index
    sheets.insert(0, ezodf.Table('SheetBeforeSheet1'))
    # get the names of all existing sheets
    sheetnames = sheets.names()
    # get count of sheets
    count = len(sheets)
    # get index of a sheet
    index = sheets.index(sheet)
    # delete a sheet by index
    del sheets[0]
    #delete a sheet by name
    del sheets['Sheet1']

Sheet Content Management
------------------------

The sheet content is managed by the :class:`Table` class. You have access to
the :class:`Cell` objects by (row, col) tuples as zero-based indices or classic
spreadsheet references (like ``'A1'`` = (0, 0)). All getters returning :class:`Cell`
objects or lists of :class:`Cell` objects.

All indices or size tuples are zero-based and have the form (row, column).

Supported operations:

* get/set table-cells
* append/insert new (empty) rows or columns
* delete rows and columns
* get whole rows or columns as standard python lists
* reset sheet content and size

metrics and property examples::

    sheet = spreadsheet.sheets['Sheet1']
    # get count of rows/columns
    rowcount = sheet.nrows()
    colcount = sheet.ncols()
    # get/set sheetname
    sheet.name = 'NewSheetName'
    # reset sheet content
    sheet.reset(size=(20, 10))

get/set table data::

    # get/set cells
    cell = table[0, 0]
    cell = table['A1']
    # set as float
    if table[0, 0].value > 100.:
        table['A1'].set_value(100.)
    # set as currency
    table['B1'].set_value(100, currency='EUR')
    # set as string
    table['C1'].set_value('Text')

    # get rows/columns
    for cell in table.column(0):
        print cell.value
    for cell in table.row(0):
        print cell.value
    # iterate over all cells
    for row in table.rows():
        for cell in row:
            print cell.value


row and column management::

    # append empty rows/columns
    table.append_rows(2)
    table.append_columns(2)
    # insert empty rows/columns
    table.insert_rows(index=5, count=2)
    table.insert_columns(index=5, count=2)
    # delete rows/columns
    table.delete_rows(index=5, count=2)
    table.delete_columns(index=5, count=2)

.. warning::

    insert/delete operations break cell references in formulas

get row and column infos (see :class:`TableRow` and :class:`TableColumn`)::

    colinfo = table.column_info(0)
    rowinfo = table.row_info(0)


