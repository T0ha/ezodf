.. module:: whitespaces

Whitespace Encoding/Decoding
============================

If the paragraph element or any of its child elements contains white-space
characters, they are collapsed. Leading white-space characters at the
paragraph start as well as trailing white-space characters at the paragraph
end are ignored. In detail, the following conversions take place:

The following `UNICODE` characters are normalized to a SPACE character:

- HORIZONTAL TABULATION (0x0009)
- CARRIAGE RETURN (0x000D)
- LINE FEED (0x000A)
- SPACE (0x0020)

In addition, these characters are ignored if the preceding character is a
white-space character. The preceding character can be contained in the same
element, in the parent element, or in the preceding sibling element, as long
as it is contained within the same paragraph element and the element in which
it is contained processes white-space characters as described above. Whitespace
characters at the start or end of the paragraph are ignored, regardless
whether they are contained in the paragraph element itself, or in a child
element in which white-space characters are collapsed as described above.

These white-space processing rules shall enable authors to use white-space
characters to improve the readability of the XML source of an OpenDocument
document in the same way as they can use them in HTML.
In other words they are processed in the same way that `HTML4` processes them.

Space Character
---------------

In general, consecutive white-space characters in a paragraph are collapsed.
For this reason, there is a special class :class:`Spaces` used to represent
the `UNICODE` character SPACE (0x0020).

.. class:: Spaces(count=1, xmlnode=None)

   This element is required to represent the second and all following SPACE
   characters in a sequence of SPACE characters.

Tab Character
-------------

.. class:: Tabulator(xmlnode=None)

   This class represents the `UNICODE` tab character HORIZONTAL TABULATION
   (0x0009) in a heading or paragraph. A :class:`Tabulator` class reserves
   space from the current position up to the next tab-stop, as defined in the
   paragraph's style information.


Line Breaks
-----------

.. class:: LineBreak(xmlnode=None)

The :class:`LineBreak` class represents a line break in a heading or paragraph.

Soft Page Break
---------------

.. class:: SoftPageBreak(xmlnode=None)

The :class:`SoftPageBreak` class represents a soft page break within a heading
or paragraph.

Soft Hyphens, Hyphens, and Non-breaking Blanks
-----------------------------------------------

Soft hyphens, hyphens, and non-breaking blanks are represented by `UNICODE`
characters.

=========================== =======================
The `UNICODE` character     Represents
=========================== =======================
SOFT HYPHEN (00AD)          soft hyphens
NON-BREAKING HYPHEN (2011)  non-breaking hyphens
NO-BREAK SPACE (00A0)       non-breaking blanks
=========================== =======================