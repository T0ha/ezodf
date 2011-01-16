.. module:: text

Text Document
=============

Span Class
----------

.. class:: Span(text="", stylename="", xmlnode=None)

   extends the :class:`~base.GenericWrapper` class.

   The :class:`Span` element represents portions of text that are attributed
   using a certain text style. The content of this element is the
   text that uses the text style. The name of the text style is the value of the
   :attr:`Span.stylename` attribute. These attribute must refer to a text style.
   :class:`Span` elements can be nested.

   Whitespace encoding is applied to the `text` parameter.
   (see :ref:`whitespace_encoding`)

Attributes
~~~~~~~~~~

.. attribute:: Span.textlen (read)

   Count of charcters of the plain text representation.

.. attribute:: Span.stylename (read/write)

   Name of the associated style.

Methods
~~~~~~~

.. method:: Span.plaintext()

   Get the plain text representation of this element. Whitespace decoding
   is applied (see :ref:`whitespace_encoding`).

.. method:: Span.append_text(text)

   Append `text` to this element. Whitespace encoding is applied.
   (see :ref:`whitespace_encoding`)

Paragraph Class
---------------

.. class:: Paragraph(text="", stylename="", xmlnode=None)

   extends the :class:`Span` class.

   Paragraphs are the basic unit of text. Whitespace encoding is applied to
   the `text` parameter. (see :ref:`whitespace_encoding`)

Heading Class
-------------

.. class:: Heading(text="", outline_level=1, stylename="", xmlnode=None)

   extends the :class:`Span` class.

   Headings define the chapter structure for a document. A chapter or subchapter
   begins with a heading and extends to the next heading at the same or higher
   level. Whitespace encoding is applied to the `text` parameter.
   (see :ref:`whitespace_encoding`)

Attributes
~~~~~~~~~~

.. attribute:: Heading.outline_level (read/write)

   The :attr:`~text.Heading.outline_level` attribute determines the level
   of the heading, starting with 1.

.. _whitespace_encoding:

Hyperlink Class
---------------

.. class:: Hyperlink(href, text="", stylename="", xmlnode=None)

   extends the :class:`Paragraph` class.

   Represents `hyperlinks` in text documents. The parameter `href` is the
   URL of the target location of this link. The `text` parameter is the link
   text. The :class:`Hyperlink` class can contain the same objects as the
   :class:`Paragraph` class.

Attributes
~~~~~~~~~~

.. attribute:: Hyperlink.name (read/write)

   A hyperlink can have a name, but it is not essential. The :attr:`~Hyperlink.name`
   attribute specifies the name of the hyperlink if one exists. This name can
   serve as a target for some other hyperlinks.

.. attribute:: Hyperlink.href (read/write)

   Specifies the URL for the target location of the link.

.. attribute:: Hyperlink.target_frame (read/write)

   Specifies the target frame of the link. This attribute can have one of the
   following values:

   ============ =============================================================
   Target Name  Location
   ============ =============================================================
   ``_self``    The referenced document replaces the content of the current
                frame.
   ``_blank``   The referenced document is displayed in a new frame.
   ``_parent``  The referenced document is displayed in the parent frame of
                the current frame.
   ``_top``     The referenced document is displayed in the uppermost frame,
                that is the frame that contains the current frame as a child
                or descendent but is not contained within another frame.
   A frame name The referenced document is displayed in the named frame. If
                the named frame does not exist, a new frame with that name is
                created.
   ============ =============================================================

Whitespace Encoding/Decoding
----------------------------

**Encoding**

Multiple spaces are replaced by the :class:`~whitespaces.Spaces` class, ``'\t'``
is replaced by the :class:`~whitespaces.Tabulator` class and ``'\n'`` is
replaced by the :class:`~whitespaces.LineBreak` class.

**Decoding**

The :class:`~whitespaces.Spaces` class is replaces by space
characters, the :class:`~whitespaces.Tabulator` class is replaced by the
``'\t'`` character and the :class:`~whitespaces.LineBreak` class is replaced
by the ``'\n'`` character.

.. toctree::
   :maxdepth: 2

   whitespaces.rst