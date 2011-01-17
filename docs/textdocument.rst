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

NumberedParagraph Class
-----------------------

.. class:: NumberedParagraph(paragraph=None, xmlnode=None)

   :param paragraph: :class:`Paragraph` or :class:`Heading` object

   In some instances, it is desirable to specify a list not as a structural
   element comprising of several list items, but to determine on a per-paragraph
   level whether the paragraph is numbered, and at which level. To facilitate
   this, the :class:`NumberedParagraph` class allows the numbering of an
   individual paragraph, as if it was part of a list at a specified level.

   Numbered paragraphs may use the same continuous numbering properties that
   list items use, and thus form an equivalent, alternative way of specifying
   lists.

   The :class:`NumberedParagraph` class contains exact one :class:`Paragraph`
   object or one :class:`Heading` object.

Attributes
~~~~~~~~~~

.. attribute:: NumberedParagraph.content (read)

   Returns the associated paragraph or heading object, or if no paragraph or
   heading object exists, a new paragraph object will be created.

.. attribute:: NumberedParagraph.level (read/write)

   A numbered paragraph can be assigned a list level. A numbered paragraph is
   equivalent to a list nested to the given level, containing one list item
   with one paragraph. If no level is given, the numbered paragraph is
   interpreted as being on level 1.

.. attribute:: NumberedParagraph.start_value (read/write)

   The attribute :attr:`~text.NumberedParagraph.start_value` may be used to
   restart the numbering of the current paragraphs's level, by setting a new
   value for the numbering.

.. attribute:: NumberedParagraph.formatted_number (read/write)

   If a numbering is applied, the text of the formatted number can
   be included. This text can be used by applications that do not support
   numbering of paragraphs, but it will be ignored by applications that
   support numbering.

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

   The OpenDocument format supports list structures, similar to those found in
   `HTML4`. A list is a paragraph-level element, which contains an optional
   list header, followed by a sequence of list items. The list header and
   each list item contains a sequence of paragraph or list elements. Lists
   can be nested.

   Lists may be numbered. The numbering may be restarted with a specific
   numbering at each list item. Lists may also continue numbering from other
   lists, allowing the user to merge several lists into a single, discontinuous
   list. Note that whether the list numbering is displayed depends on a
   suitable list style being used.

   Every list has a list level, which is determined by the nesting of the
   :class:`~text.List` elements. If a list is not contained within another
   list, the list level is 1. If the list in contained within another list,
   the list level is the list level of the list in which is it contained
   incremented by one. If a list is contained in a table cell or text box,
   the list level returns to 1, even though the table or textbox itself may
   be nested within another list.

Attributes
~~~~~~~~~~

.. attribute:: List.style_name (read/write)

   Specifies the name of the list style that is applied to the list.

   If this attribute is not included and therefore no list style is specified,
   one of the following actions is taken:

   * If the list is contained within another list, the list style defaults to
     the style of the surrounding list.
   * If there is no list style specified for the surrounding list, but the
     list contains paragraphs that have paragraph styles attached specifying
     a list style, this list style is used for any of these paragraphs.
   * A default list style is applied to any other paragraphs.

.. attribute:: List.continue_numbering (read/write)

   By default, the first list item in a list starts with the number specified
   in the list style. The continue numbering attribute can be used to continue
   the numbering from the preceding list.

   This attribute can have a value of `True` or `False`.

   If the value of the attribute is `True` and the numbering style of the
   preceding list is the same as the current list, the number of the first
   list item in the current list is the number of the last item in the
   preceding list incremented by one.

.. attribute:: List.header (read/write)

   Set/Get the :class:`~text.ListHeader` object.

Methods
~~~~~~~

.. method:: List.iteritems()

   Iterate over all list items.

ListItem Class
--------------

.. class:: ListItem(text="", xmlnode=None)

   List items contain the textual content of a list. A :class:`ListItem`
   element can contain :class:`Paragraph`, :class:`Heading`, :class:`List`
   or :class:`~whitespaces.SoftPageBreak`. A list item **cannot contain tables.**

   The first line in a list item is preceded by a bullet or number, depending
   on the list style assigned to the list. If a list item starts another list
   immediately and does not contain any text, no bullet or number is displayed.

Attribute
~~~~~~~~~

.. attribute:: ListItem.start_value (read/write)

   The numbering of the current list can be restarted at a certain number.
   The :attr:`~text.ListItem.start_value` attribute is used to specify the
   number with which to restart the list. This attribute can only be applied
   to items in a list with a numbering list style. It restarts the numbering
   of the list at the current item.

.. attribute:: ListItem.formatted_number (read/write)

   If a numbering is applied, the text of the formatted number can
   be included. This text can be used by applications that do not support
   numbering of lists, but it will be ignored by applications that
   support numbering.

ListHeader Class
----------------

.. class:: ListHeader(text="", xmlnode=None)

   A list header is a special kind of list item. It contains one or more
   paragraphs that are displayed before a list. The paragraphs are formatted
   like list items but they do not have a preceding number or bullet. The
   list header is represented by the list header element.

Section Class
-------------

.. class:: Section(name="", style_name="", xmlnode=None)

   A text section is a named region of paragraph-level text content. Sections
   start and end on paragraph boundaries and can contain any number of paragraphs.

   Sections have two uses in the OpenDocument format: They can be used to
   assign certain formatting properties to a region of text. They can also be
   used to group text that is automatically acquired from some external data
   source.

   In addition to Sections can contain regular text content or the text can
   be contained in another file and linked to the section. Sections can also
   be write-protected or hidden.

   Sections can have settings for text columns, background color or pattern,
   and notes configuration.

   Sections support two ways of linking to external content. If a section is
   linked to another document, the link can be through one of the following:

   * A resource identified by an XLink, represented by a :class:`SectionSource` element
   * Dynamic Data Exchange (DDE), represented by a :class:`DDESource` element

   Linking information for external content is contained in the section
   element's first child. A section that links to external content contains
   the full representation of the data source, so that processors need to
   understand the linking information only if they wish to update the contents
   of the section.

Attributes
~~~~~~~~~~

.. attribute:: Section.style_name (read/write)

   Refers to the section style.

.. attribute:: Section.name (read/write)

   Every section must have a name that uniquely identifies the section.

.. attribute:: Section.protected (read/write)

   A section can be protected, which means that a user can not edit the
   section. The :attr:`~Section.protected` attribute indicates whether or not
   a section is protected. If `True` a random password hash will be set, so
   editing is not possible.

.. _whitespace_encoding:

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