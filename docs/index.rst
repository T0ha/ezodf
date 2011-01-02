.. ezodf documentation master file, created by
   sphinx-quickstart on Thu Dec 30 16:01:08 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ezodf's documentation!
=================================

**ezodf** is a Python package to create new or open existing OpenDocumentFormat
files to extract, add, modify or delete document data.

To open an existing document, just use the :func:`ezodf.open` function::

    doc = ezodf.open('documentname.ext')

You don't have to care about the document type on open, to check the type of
the document you got, use the **mimetype** attribute::

    if doc.mimetype == ezodf.const.MIMETYPES['odt']:
        # this is a text document
        # and so on for 'ods', 'odg' or 'odg'

To change the meta data of the document use the **meta** attribute,
which is an instance of the :ref:`Meta class`::

   document_titel = doc.meta['title']
   # or set meta attributes
   doc.meta['description'] = 'set a new description'

For more information about meta data see the :ref:`meta module` .

Contents:

.. toctree::
   :maxdepth: 1

   intro.rst

   meta.rst
   styles.rst
   content.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

