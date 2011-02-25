.. module:: document

Document Classes
================

Packaged Document
-----------------

.. class:: PackagedDocument()

   The :class:`PackagedDocument` manages a zip-packed ODF document.

.. warning::

   Don't create instances of this class by yourself, always use :func:`ezodf.opendoc`
   and :func:`ezodf.newdoc` to open or create documents.

Attributes
~~~~~~~~~~

.. attribute:: PackagedDocument.backup (read/write)

   `True` or `False`: Create backup files on :meth:`~PackagedDocument.save()`
   and :meth:`~PackagedDocument.saveas()`.

.. attribute:: PackagedDocument.docname (read/write)

   The file system filename, `None` if not set.

.. attribute:: PackagedDocument.doctype (read)

   The document doctype is a three character string like the usual file
   extensions (``'odt'`` for text, ``'ods'`` for spreadsheets and so on, see
   also :ref:`doctype_table`)

.. attribute:: PackagedDocument.mimetype (read)

   The document mimetype (see also :ref:`doctype_table`)

.. attribute:: PackagedDocument.meta

   see :class:`meta.Meta`

.. attribute:: PackagedDocument.styles

.. attribute:: PackagedDocument.body

Methods
~~~~~~~

.. method:: PackagedDocument.save()

   Save document to file system.

.. method:: PackagedDocument.saveas(filename)

   Save document to file system with a new `filename`.

.. method:: PackagedDocument.tobytes()

   Get the document zip-file as `bytes`.

Flat XML Document
-----------------

.. class:: FlatXMLDocument(filetype='odt', filename=None)

   The :class:`FlatXMLDocument` manages a single-XML-file ODF document.

.. warning::

   Don't create instances of this class by yourself, always use
   :func:`ezodf.opendoc` and :func:`ezodf.newdoc` to open or create documents.

Attributes
~~~~~~~~~~

.. attribute:: FlatXMLDocument.doctype

   see :attr:`PackagedDocument.doctype`

.. attribute:: FlatXMLDocument.mimetype

   see :attr:`PackagedDocument.mimetype`

Methods
~~~~~~~

.. method:: FlatXMLDocument.save()

   see :func:`PackagedDocument.save`

.. method:: FlatXMLDocument.saveas(filename)

   see :func:`PackagedDocument.saveas`
