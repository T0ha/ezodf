.. _opendoc:

Document Management
===================

Open an existing Document
-------------------------

.. function:: ezodf.opendoc(filename)

   :param str filename: filename of the document
   :returns: :class:`PackagedDocument` or :class:`FlatXMLDocument`

   Open the document `filename`. Returns an instance of the :class:`PackagedDocument`
   class, if the file is a zip-packed document, or an instance of the
   :class:`FlatXMLDocument` class, if the document is a single-XML-file document.
   The document type is determined by the file content.

   You can check the document type by the :attr:`~PackagedDocument.doctype` or the
   :attr:`~PackagedDocument.mimetype` attribute.

.. _newdoc:

Create a new Document
---------------------

.. function:: ezodf.newdoc(doctype="odt", filename="", template=None)

  :param str doctype: document type, three character string like the usual file
    extensions (``'odt'`` for text, ``'ods'`` for spreadsheets and so on)
  :param str filename: filename of the document, can also be set by the
    :func:`~PackagedDocument.saveas()` method
  :param str template: filename of a template file, it has to be a zip-packed
    document and the parameter `doctype` is ignored, because the template content
    determines the document type.
  :returns: :class:`PackagedDocument`

  Create a new ODF Document. Returns always an instance of the
  :class:`PackagedDocument` class.

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

Data model
----------

I use the `lxml <http://codespeak.net/lxml/>`_ package to manage the XML data.
You have access to the `lxml` Elements by the **xmlnode** attribute all classes.
All document classes have the attributes **meta**, **styles**,
**manifest** and **content** and each of them have a **xmlnode** attribute to
the XML representation of the associated XML files `manifest.xml`, `styles.xml`,
`meta.xml` and `content.xml`.
