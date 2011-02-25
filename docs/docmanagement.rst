Document Management
===================

.. _opendoc:

Open an existing Document
-------------------------

.. function:: ezodf.opendoc(filename)

   :param str filename: a filename  or the file-content as `bytes`
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

.. _newdoc:

Create a new Document
---------------------

.. function:: ezodf.newdoc(doctype="odt", filename="", template=None)

  :param str doctype: document type, three character string like the usual file
    extensions (``'odt'`` for text, ``'ods'`` for spreadsheets and so on)
  :param str filename: filename of the document, can also be set by the
    :func:`~document.PackagedDocument.saveas()` method
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
