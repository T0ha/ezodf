
Abstract
========

**ezodf** is a Python package to create new or open existing OpenDocument
(ODF) files to extract, add, modify or delete document data.

a simple example::

    from ezodf import newdoc, Paragraph, Heading, Sheet

    odt = newdoc(doctype='odt', filename='text.odt')
    odt.body += Heading("Chapter 1")
    odt.body += Paragraph("This is a paragraph.")
    odt.save()

    ods = newdoc(doctype='ods', filename='spreadsheet.ods')
    sheet = Sheet('SHEET', size=(10, 10))
    ods.sheets += sheet
    sheet['A1'].set_value("cell with text")
    sheet['B2'].set_value(3.141592)
    sheet['C3'].set_value(100, currency='USD')
    sheet['D4'].formula = "of:=SUM([.B2];[.C3])"
    pi = sheet[1, 1].value
    ods.save()

for more examples see: /examples folder

Dependencies
============

* lxml <http://codespeak.net/lxml/> for painless serialisation with prefix
  declaration (xlmns:prefix="global:namespace:specifier") in the root element.
  Declarations for unused prefixes are also possible.

The target platform is CPython 2.7 and CPython 3.3+, work on compability with 
CPython 2.6 is in progress.

Installation
============

with pip::

    pip install ezodf

or from source::

    python setup.py install

Documentation
=============

http://packages.python.org/ezodf

send feedback to t0hashvein@gmail..com

ezodf can be found on GitHub at:

https://github.com/T0ha/ezodf
