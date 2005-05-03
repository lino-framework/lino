# -*- coding: Latin-1 -*-
## Copyright 2005 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
import sys

from lino.misc.tsttools import TestCase, main, catch_output
from lino.tools.textsplitter import TextSplitter
from lino.tools import guesscoding 


TESTDATA = os.path.join(os.path.dirname(__file__),"testdata")

class Case(TestCase):
    def test01(self):
        
        splitter = TextSplitter()
        
        s = open(os.path.join(TESTDATA,"gnosis-readme")).read()
        self.assertEqual(len(s), 1662)

        words = splitter.split(s)
        self.assertEqual(len(words), 193)
        #print " ".join(words)
        self.assertEquivalent(" ".join(words), """
GNOSIS UTILITIES CONTAINS SEVERAL SUBPACKAGES FOR WORKING WITH XML WELL OTHER GENERALLY USEFUL TOOLS THE MAJOR MODULES ARE GNOSIS INDEXER FULL TEXT INDEXING SEARCHING GNOSIS XML PICKLE XML PICKLING PYTHON OBJECTS GNOSIS XML OBJECTIFY ANY XML NATIVE PYTHON OBJECTS GNOSIS XML VALIDITY ENFORCE VALIDITY CONSTRAINTS GNOSIS XML RELAX TOOLS FOR WORKING WITH RELAXNG GNOSIS XML INDEXER XPATH INDEXING XML DOCUMENTS CONVERT ASCII SOURCE FILES HTML GNOSIS UTIL DTD2SQL DTD SQL CREATE TABLE STATEMENTS GNOSIS UTIL SQL2DTD SQL QUERY DTD FOR QUERY RESULTS GNOSIS UTIL XML2SQL XML SQL INSERT INTO STATEMENTS GNOSIS UTIL COMBINATORS COMBINATORIAL HIGHER ORDER FUNCTIONS GNOSIS UTIL INTROSPECT INTROSPECT PYTHON OBJECTS GNOSIS MAGIC MULTIMETHODS METACLASSES ETC INSTALLATION PYTHON SETUP BUILD PYTHON SETUP INSTALL TRYING OUT GNOSIS XML PICKLE TEST PYTHON TEST ALL SIMILARLY FOR OTHER SUBPACKAGES ANY ERRORS OCCUR PLEASE EMAIL MERTZ GNOSIS FRANKM HIWAAY NET PLEASE INCLUDE THE OUTPUT FROM TEST ALL YOUR EMAIL WELL OTHER PERTINENT DETAILS SUCH PYTHON VERSION AND OPERATING SYSTEM FOR MORE INFO PYDOC GNOSIS PYDOC GNOSIS XML PICKLE DOC SEE XML MATTERS ARTICLES UNDER GNOSIS DOC YOU ARE USING PYTHON YOU MUST FIRST INSTALL NEWER VERSION PYXML SEE YOU DON HAVE ANYTHING FOR PYTHON AND
        """)
        
        fname = os.path.join(TESTDATA,"cp850a.txt")
        s = open(fname).read()
        self.assertEqual(len(s), 364)
        #print s
        #s = guesscoding.decode(s)
        s = guesscoding.recode(s,sys.getdefaultencoding())
        print s
        words = splitter.split(s)
        self.assertEqual(len(words), 48)
        print " ".join(words)
        self.assertEquivalent(" ".join(words), """
        """)
    
if __name__ == '__main__':
    main()

