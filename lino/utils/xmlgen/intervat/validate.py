# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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


USAGE = """
Usage:

  python -m lino.utils.intervat.validate SCHEMA XMLFILE

Arguments:

SCHEMA : the schema to validate against. Possible values are:

  id  internal name            French name
  --- ------------------------ --------------------------------
  clc ClientListingConsignment Liste des clients assujettis
  ico IntraConsignment         Liste des clients intracommunautaires
  --- ------------------------ --------------------------------
  
XMLFILE : the name of the xml file to validate, or '-' to read from stdin
"""

if __name__ == '__main__':

    import sys
    from lxml import etree
    from lino.utils import intervat

    if len(sys.argv) < 3:
        #~ raise Exception("Usage: python -m %s name of the file to be validated" % __name__)
        #~ raise Exception("Missing command-line argument: the name of the file to be validated.")
        print USAGE
        sys.exit(-1)
    nsname = sys.argv[1]
    fn = sys.argv[2]
    
    ns = getattr(intervat,nsname,None)
    if ns is None:
        print "Invalid type %r" % nsname 
        sys.exit(-1)
        
    doc = etree.parse(fn)
    ns.validate_doc(doc)
    print fn, "is a valid %s" % ns.__class__.__name__