.. module:: text

Text Document
=============

Span Class
----------

.. class:: Span(text="", stylename="")

   extends the :class:`~base.GenericWrapper` class.

   The :class:`Span` element represents portions of text that are attributed
   using a certain text style or class. The content of this element is the
   text that uses the text style. The name of the text style is the value of the
   :attr:`Span.stylename` attribute. These attribute must refer to a text style.
   :class:`Span` elements can be nested.

Attributes
~~~~~~~~~~

.. attribute:: Span.textlen (read)

.. attribute:: Span.stylename (read/write)

Methods
~~~~~~~

.. method:: Span.plaintext()

.. method:: Span.append_plaintext()

Paragraph Class
---------------

.. class:: Paragraph

   extends the :class:`Span` class.

   Paragraphs are the basic unit of text.

Heading Class
-------------

.. class:: Heading

   extends the :class:`Span` class.

   Headings define the chapter structure for a document. A chapter or subchapter
   begins with a heading and extends to the next heading at the same or higher
   level.

Attributes
~~~~~~~~~~

.. attribute:: Heading.outline_level (read/write)

.. whitespace_encoding:

Whitespace Encoding
-------------------
