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
from lino.tools import textsplitter
from lino.tools import guesscoding 


TESTDATA = os.path.join(os.path.dirname(__file__),"testdata")

class Case(TestCase):
    skip=True # textsplitter is frozen
    def test01(self):


        for coding in ("cp850","cp1252"):

            sp = textsplitter.TextSplitter(coding)

            #print sp.xalphas.encode("ascii","replace")
            s = sp.xalphas.decode(coding)
            print coding, ":", s.encode(sys.getdefaultencoding(),"replace")
        
##         ustrings = []
##         for coding in ("cp850","cp1252"):
##             # cp850b.txt contains all non-ascii alphabetic chars I have
##             # ever encountered in cp850:
##             s = open(os.path.join(TESTDATA,enc+"b.txt")).read().strip()

##             l = map(ord,[ch for ch in s])

##             # print l
        
##             self.assertEqual(textsplitter.xalphas[enc], s)

##             ustrings.append(s.decode(coding))

##         for us in ustrings:
##             for ch in us:
##                 self.failUnless(ch.isalpha())

        boxchar = chr(179).decode("cp850")
        # print repr(boxchar)
        self.failIf(boxchar.isalpha())
    
if __name__ == '__main__':
    main()

