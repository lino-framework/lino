# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Luc Saffre
# License: BSD (see file COPYING for details)


USAGE = """
Validate a XML file against the XSD for a SEPA payment order.

Usage::

  python -m lino.utils.xmlgen.sepa.validate XMLFILE

Arguments:
 
XMLFILE : the name of the xml file to validate, or '-' to read from stdin
"""

import sys
from os.path import join, dirname
from lxml import etree

def validate_pain001(xmlfile):
    doc = etree.parse(open(xmlfile))
    xsdfile = join(dirname(__file__), 'XSD', 'pain.001.001.02.xsd')
    xsd = etree.XMLSchema(etree.parse(open(xsdfile)))
    xsd.assertValid(doc)
    
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(-1)

    validate_pain001(sys.argv[1])
    
