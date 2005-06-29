# coding: latin1
## Copyright 2003-2005 Luc Saffre

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

from lino.misc.tsttools import TestCase, main, Toolkit

from lino.console import syscon

from lino.apps.keeper.keeper import Keeper
from lino.apps.keeper.tables import *

TESTDATA = os.path.join(
    os.path.dirname(__file__),"testdata")

class Case(TestCase):
    #todo="VolumeVisitor instance has no attribute 'reloading'"
    def test01(self):
        app=Keeper()
        sess=app.quickStartup() # toolkit=Toolkit())
        
        q=sess.query(Volumes)
        vol=q.appendRow(name="test",path=TESTDATA)
        vol.load(sess)
        sess.showQuery(
            vol.directories,
            columnNames="id name parent files subdirs",
            width=70)
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""\
Directories (volume=testparent=None)
====================================
id     |name          |parent        |files         |subdirs
-------+--------------+--------------+--------------+--------------
1      |              |              |17 Files      |4 Directories
""")
        sess.shutdown()
        
        
if __name__ == '__main__':
    main()

