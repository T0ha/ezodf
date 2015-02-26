Document Management
===================

.. _global_configuration:

Global Configuration
--------------------

.. attribute:: ezodf.config

    The *global Configuration* object provides several configuration methods.

.. automethod:: ezodf.config.set_table_expand_strategy

.. automethod:: ezodf.config.reset_table_expand_strategy

.. _opendoc:

Open an existing Document
-------------------------

.. function:: ezodf.opendoc(filename)

   :param filename: a filename  or the file-content as file-like object (`StringIO` or `BytesIO`)
   :type filename: str or StringIO or BytesIO 
   :returns: :class:`~document.PackagedDocument` or :class:`~document.FlatXMLDocument`

   Open the document `filename`. Returns an instance of the :class:`~document.PackagedDocument`
   class, if the file is a zip-packed document, or an instance of the
   :class:`~document.FlatXMLDocument` class, if the document is a single-XML-file document.
   The document type is determined by the file content.

   If you have no access to the filesystem, pass the content of the zip-file
   (type `bytes`) as filename parameter. The :meth:`~document.PackagedDocument.save`
   method still works, but no backups will be created.

   You can check the document type by the :attr:`~document.PackagedDocument.doctype` or the
   :attr:`~document.PackagedDocument.mimetype` attribute.

.. _openods:

Open Spreadsheets
-----------------

Desktop applications often adding many empty rows and/or empty columns and
this library has a very simple cell management strategy - every cell is
represented in RAM in a 2-dimensional array - which can fill the whole memory.
I have added three different opening strategies for spreadsheets
and tables to prevent a memory overflow.

Because loading spreadsheets is an automatic class wrapping
process and there is no simple way to pass additional parameters to the
opening process (a library design error, sorry), you have to configure
the opening strategy by the :ref:`global_configuration` object.

The three strategies are:

- expand strategy = ``'all'`` - expand all cells - can cause a memory overflow
- expand strategy = ``'all_but_last'`` - expand all cells but last row/column,
  better, but sometimes the penultimate row/column blow up the memory
- expand strategy = ``'all_less_maxcount'`` - expand all rows/columns with less
  than *maxcount* repetitions, rows/columns with maxcount or more repetitions
  are replaced by *one* row/column. This is the default strategy, where
  ``maxcount=(32, 32)``, to set the global parameters see :ref:`global_configuration`
  object.

.. warning::

  Only the strategy ``'all'`` guarantee the original spreadsheet layout, the
  other two strategies can break cell references and other strange things
  can happen, but in most cases they only remove unnecessary appended rows and
  columns.

example::

    import ezodf

    # if it is necessary to expand all rows/columns
    ezodf.config.set_table_expand_strategy('all')

    spreadsheet = ezodf.opendoc('expand_all_cells.ods')

    # advice: always reset table expanding strategy
    ezodf.config.reset_table_expand_strategy()


.. _newdoc:


Create a new Document
---------------------

.. function:: ezodf.newdoc(doctype="odt", filename="", template=None)

  :param str doctype: document type, three character string like the usual file
    extensions (``'odt'`` for text, ``'ods'`` for spreadsheets and so on)
  :param filename: filename or file-like object of the document, can also be set by the
    :func:`~document.PackagedDocument.saveas()` method
  :type filename: str or StringIO or BytesIO 
  :param str template: filename of a template file or the file-content as
    `bytes`, it has to be a zip-packed document and the parameter `doctype`
    is ignored, because the template content determines the document type.
  :returns: :class:`~document.PackagedDocument`

  Create a new ODF Document. Returns always an instance of the
  :class:`~document.PackagedDocument` class.

  If you have no access to the filesystem, pass the content of the zip-file
  (type `bytes`) as filename parameter.

.. _doctype_table:

Doctype Table
-------------

======= ========================================================================
Doctype Mimetype
======= ========================================================================
odt     application/vnd.oasis.opendocument.text
ott     application/vnd.oasis.opendocument.text-template
odg     application/vnd.oasis.opendocument.graphics
otg     application/vnd.oasis.opendocument.graphics-template
odp     application/vnd.oasis.opendocument.presentation
otp     application/vnd.oasis.opendocument.presentation-template
ods     application/vnd.oasis.opendocument.spreadsheet
ots     application/vnd.oasis.opendocument.spreadsheet-template
odc     application/vnd.oasis.opendocument.chart
otc     application/vnd.oasis.opendocument.chart-template
odi     application/vnd.oasis.opendocument.image
oti     application/vnd.oasis.opendocument.image-template
odf     application/vnd.oasis.opendocument.formula
otf     application/vnd.oasis.opendocument.formula-template
odm     application/vnd.oasis.opendocument.text-master
oth     application/vnd.oasis.opendocument.text-web
======= ========================================================================

Data Model
----------

I use the `lxml <http://codespeak.net/lxml/>`_ package to manage the XML data.
You have access to the :mod:`lxml` Elements by the :attr:`~base.GenericWrapper.xmlnode`
attribute in all ODF Content Wrapper classes which bases on the
:class:`~base.GenericWrapper` class.

All document classes have the attributes :attr:`~document.PackagedDocument.meta`,
:attr:`~document.PackagedDocument.styles`, :attr:`~document.PackagedDocument.manifest`,
:attr:`~document.PackagedDocument.content` and :attr:`~document.PackagedDocument.body`
and each of them have a :attr:`xmlnode` attribute to the XML representation
of the associated XML files `manifest.xml`, `styles.xml`, `meta.xml` and
`content.xml`.

.. toctree::
   :maxdepth: 1

   xmlns.rst
   base.rst
