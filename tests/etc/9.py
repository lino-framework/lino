# coding: latin1
## Copyright Luc Saffre 2003-2005

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

from lino.misc.tsttools import TestCase, main

from lino.apps.keeper.keeper import Keeper
from lino.apps.keeper.keeper_tables import *

from lino.forms.testkit import Toolkit

TESTDATA = os.path.join(os.path.dirname(__file__),"testdata")

class Case(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
        self.app=Keeper(toolkit=Toolkit(console=self.ui))
        #self.app.run_forever()
        self.app.init()
        
    def tearDown(self):
        self.app.close()
        
    def test01(self):
        s=self.getConsoleOutput()
        print s
        self.assertEquivalent(s,"""\
        """)
        
        q=self.app.sess.query(Volumes)
        vol=q.appendRow(name="foo",path=TESTDATA)
        vol.load(self.ui)
        vol.directories.report()
        s=self.getConsoleOutput()
        print s
        self.assertEquivalent(s,"""\
        """)
        
        
if __name__ == '__main__':
    main()

