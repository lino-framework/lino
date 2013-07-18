#!/usr/bin/env python
# -*- coding: utf-8 -*- 
## Copyright 2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
"""

import os
import sys
#~ from xml.dom import minidom
from lxml import etree


XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema"
XSD = "{%s}" % XSD_NAMESPACE

NSMAP = dict(xsd=XSD_NAMESPACE)


def xsdnames(fn,nsname):
    tree = etree.parse(fn) 
    root = tree.getroot()
    names = set()
    def collect(e):
        na = e.get('name',None)
        if na is not None:
            names.add(na)
        for child in e:
            collect(child)
    collect(root)
    return ' '.join(names)


def main(fn):
    print xsdnames(fn,'ns0')

if __name__ == "__main__":
    main(sys.argv[1])
