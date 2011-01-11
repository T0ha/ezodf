
Abstract
========

**ezodf** is a Python package to create new or open existing OpenDocument
(ODF) files to extract, add, modify or delete document data.

a simple example::

    import ezodf

    # this ODS example doesn't work yet
    ods = ezodf.newdoc(doctype='ods', 'spreadsheet.ods')
    # document content resides in the body object
    sheet = ods.body.add(ezodf.Spreadsheet('SHEET'))
    sheet[0, 0] = ezodf.Paragraph("Textcell")
    ods.save()

    # this simple ODT example works
    odt = ezodf.newdoc(doctype='odt', 'text.odt')
    paragraph = ezodf.Paragraph("This is a paragraph. ")
    # document content resides in the body object
    odt.body.add(paragraph)
    paragraph.append_plaintext("This is another sentence.\nNormal useage of line breaks.")
    odt.body.add(ezodf.Heading("Chapter 1"), insert_before=paragraph)
    odt.save()

for more examples see: /examples folder

Dependencies
============

* lxml <http://codespeak.net/lxml/> for painless serialisation with prefix
  declaration (xlmns:prefix="global:namespace:specifier") in the root element.
  Declarations for unused prefixes are also possible.

The target platform is Python 3.1+, no Python 2 support planned at this time.

Installation
============

with pip::

    pip install ezodf

or from source::

    python setup.py install

Tests
=====

run tests ::

    python runtests.py

on Windows::

    runtests.bat

Documentation
=============

http://packages.python.org/ezodf

send feedback to mozman@gmx.at

ezodf can be found on bitbucket.org at:

http://bitbucket.org/mozman/ezodf
