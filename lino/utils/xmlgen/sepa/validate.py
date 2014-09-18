# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)


USAGE = """
Validate an XML file against the XSD for a SEPA payment order.

Usage::

  python -m lino.utils.xmlgen.sepa.validate XMLFILE

Arguments:
 
XMLFILE : the name of the xml file to validate, or '-' to read from stdin
"""

import sys
from os.path import join, dirname
from lxml import etree

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print USAGE
        sys.exit(-1)

    xmlfile = sys.argv[1]
    doc = etree.parse(file(xmlfile))

    xsdfile = join(dirname(__file__), 'XSD', 'pain.001.001.02.xsd')
    xsd = etree.XMLSchema(etree.parse(file(xsdfile)))

    xsd.assertValid(doc)
