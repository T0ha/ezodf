.. module:: text

Text Document
=============

Span Class
----------

.. class:: Span(text="", style_name="", xmlnode=None)

   extends the :class:`~base.GenericWrapper` class.

   The :class:`Span` element represents portions of text that are attributed
   using a certain text style. The content of this element is the
   text that uses the text style. The name of the text style is the value of the
   :attr:`Span.style_name` attribute. These attribute must refer to a text style.
   :class:`Span` elements can be nested.

   Whitespace encoding is applied to the `text` parameter.
   (see :ref:`whitespace_encoding`)

Attributes
~~~~~~~~~~

.. attribute:: Span.textlen (read)

   Count of charcters of the plain text representation.

.. attribute:: Span.style_name (read/write)

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

.. class:: Paragraph(text="", style_name="", xmlnode=None)

   extends the :class:`Span` class.

   Paragraphs are the basic unit of text. Whitespace encoding is applied to
   the `text` parameter. (see :ref:`whitespace_encoding`)

Attributes
~~~~~~~~~~

.. attribute:: Paragraph.cond_style_name (read/write)

   The :attr:`~Paragraph.cond_style_name` attribute references a conditional-style,
   that is, a style that contains conditions and maps to other styles. If a
   conditional style is applied to a paragraph, the :attr:`~Paragraph.style_name`
   attribute contains the name of the style that was the result of the
   conditional style evaluation, while the conditional style name itself is
   the value of the :attr:`~Paragraph.cond_style_name` attribute.

.. attribute:: Paragraph.ID (read/write)

   A paragraph may have an ID. This ID can be used to reference the paragraph
   from other elements.

NumberedParagraph Class
-----------------------

.. class:: NumberedParagraph(number, text="", style_name="", xmlnode=None)

Heading Class
-------------

.. class:: Heading(text="", outline_level=1, style_name="", xmlnode=None)

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

.. attribute:: Heading.restart_numbering (read/write)

   The numbering of headers can be restarted by setting the
   :attr:`~text.Heading.restart_numbering` attribute to `True`.

.. attribute:: Heading.start_value (read/write)

   The attribute :attr:`~text.Heading.start_value` may be used to restart the
   numbering of headers of the current header's level, by setting a new value
   for the numbering.

.. attribute:: Heading.suppress_numbering (read/write)

   It is sometimes desired to have a specific heading which should not be
   numbered. To facilitate this, set this attribute `True` and the given header
   will not be numbered.

.. attribute:: Heading.formatted_number (read/write)

   If a heading has a numbering applied, the text of the formatted number can
   be included. This text can be used by applications that do not support
   numbering of headings, but it will be ignored by applications that support
   numbering.

.. _whitespace_encoding:

Hyperlink Class
---------------

.. class:: Hyperlink(href, text="", style_name="", xmlnode=None)

   extends the :class:`Span` class.

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

List Class
----------

.. class:: List(style_name="", xmlnode=None)

ListItem Class
--------------

.. class:: ListItem(text="", xmlnode=None)

ListHeader Class
----------------

.. class:: ListHeader(text="", xmlnode=None)

Section Class
-------------

.. class:: Section(xmlnode=None)

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