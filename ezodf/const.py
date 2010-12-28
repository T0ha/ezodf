#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: const.py
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

VERSION = "0.1.0"
PACKAGENAME = "ezodf"

MIMETYPES = {
    'odt': "application/vnd.oasis.opendocument.text",
    'ott': "application/vnd.oasis.opendocument.text-template",
    'odg': "application/vnd.oasis.opendocument.graphics",
    'otg': "application/vnd.oasis.opendocument.graphics-template",
    'odp': "application/vnd.oasis.opendocument.presentation",
    'otp': "application/vnd.oasis.opendocument.presentation-template",
    'ods': "application/vnd.oasis.opendocument.spreadsheet",
    'ots': "application/vnd.oasis.opendocument.spreadsheet-template",
    'odc': "application/vnd.oasis.opendocument.chart",
    'otc': "application/vnd.oasis.opendocument.chart-template",
    'odi': "application/vnd.oasis.opendocument.image",
    'oti': "application/vnd.oasis.opendocument.image-template",
    'odf': "application/vnd.oasis.opendocument.formula",
    'otf': "application/vnd.oasis.opendocument.formula-template",
    'odm': "application/vnd.oasis.opendocument.text-master",
    'oth': "application/vnd.oasis.opendocument.text-web",
}

FILE_EXT_FOR_MIMETYPE = { mimetype:ext for ext, mimetype in MIMETYPES.items() }

ODFNS = {
    'anim': "urn:oasis:names:tc:opendocument:xmlns:animation:1.0",
    'db': "urn:oasis:names:tc:opendocument:xmlns:database:1.0",
    'chart': "urn:oasis:names:tc:opendocument:xmlns:chart:1.0",
    'config': "urn:oasis:names:tc:opendocument:xmlns:config:1.0",
    'dc': "http://purl.org/dc/elements/1.1/",
    'dom': "http://www.w3.org/2001/xml-events",
    'dr3d': "urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0",
    'draw': "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    'fo': "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
    'form': "urn:oasis:names:tc:opendocument:xmlns:form:1.0",
    'koffice': "http://www.koffice.org/2005/",
    'manifest': "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0",
    'math': "http://www.w3.org/1998/Math/MathML",
    'meta': "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
    'numbers': "urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0",
    'office': "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    'ooo': "http://openoffice.org/2004/office",
    'ooow': "http://openoffice.org/2004/writer",
    'oooc': "http://openoffice.org/2004/calc",
    'presentations': "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
    'rdfa': "http://docs.oasis-open.org/opendocument/meta/rdfa#",
    'script': "urn:oasis:names:tc:opendocument:xmlns:script:1.0",
    'smil': "urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0",
    'style': "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
    'svg': "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
    'table': "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    'text': "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    'xforms': "http://www.w3.org/2002/xforms",
    'xlinks': "http://www.w3.org/1999/xlink",
    'xml': "http://www.w3.org/XML/1998/namespace",
}
