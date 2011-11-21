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

from lino.misc.tsttools import TestCase, main
#from lino.tools.guesscoding import EncodingGuesser
from lino.tools.guessenc.guesser import EncodingGuesser


TESTDATA = os.path.join(os.path.dirname(__file__),"testdata")

class Case(TestCase):
    def test01(self):
        g = EncodingGuesser()
        filename = os.path.join(TESTDATA,"gnosis-readme")
        self.assertEqual(g.guess(filename),None)
        
        filename = os.path.join(TESTDATA,"cp850a.txt")
        self.assertEqual(g.guess(filename),"cp850")
        
        filename = os.path.join(TESTDATA,"cp850b.txt")
        self.assertEqual(g.guess(filename),"cp850")
        
        filename = os.path.join(TESTDATA,"README.TXT")
        self.assertEqual(g.guess(filename),"cp850")
        
        filename = os.path.join(TESTDATA,"cp1252a.txt")
        self.assertEqual(g.guess(filename),"cp1252")
        
        filename = os.path.join(TESTDATA,"cp1252b.txt")
        self.assertEqual(g.guess(filename),"cp1252")
        
    
if __name__ == '__main__':
    main()

