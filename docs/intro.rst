.. _intro:

Introduction
============

The main intention of the **ezodf** package is to **easy** read, write and
modify OpenDocumentFormat files but without the goal to support all possibilities
that the OASIS OpenDocument Standard provides.

To be clear, it is safe to open and rewrite ODF files with unsupported features,
thanks to the documented container format (PKZIP format) and the XML technology
nothing get lost, even non-standard data in the container file is copied.

OpenDocument (ODF)
------------------

The Open Document Format for Office Applications (also known as OpenDocument
or ODF) is an XML-based file format for representing electronic documents
such as spreadsheets, charts, presentations and word processing documents.

While the specifications were originally developed by Sun Microsystems, the
standard was developed by the OASIS Open Document Format for Office Applications
(OpenDocument) TC - OASIS ODF TC, committee of the Organization for the
Advancement of Structured Information Standards (OASIS) consortium and based
on the XML format originally created and implemented by the OpenOffice.org
office suite.

In addition to being an OASIS standard, it is published (in one of its version
1.0 manifestations) as an ISO/IEC international standard, ISO/IEC 26300:2006
Open Document Format for Office Applications (OpenDocument) v1.0.

.. seealso:: https://secure.wikimedia.org/wikipedia/en/wiki/OpenDocument

Data model
----------

I use the `lxml <http://codespeak.net/lxml/>`_ package to manage the XML data.
You have access to the `lxml` Elements by the **xmlroot** attribute at the most
classes. All document classes have the attributes **meta**, **styles**,
**manifest** and **content** and each of them have a **xmlroot** attribute to
the XML representation of the associated XML files `manifest.xml`, `styles.xml`,
`meta.xml` and `content.xml`.