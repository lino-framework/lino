#coding: latin1
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

from lino.misc import tsttools
from lino.scripts import pds2sxw, pds2sxc

class Case(tsttools.TestCase):
    todo="pds2sxw and pds2sxc don't work"
    def test01(self):
        fn = self.addTempFile("5.sxw",showOutput=True)
        pds2sxw.main(["-o", fn, "-b", "5.pds"])
        
    def test02(self):
        fn = self.addTempFile("5b.sxw")
        pds2sxw.main(["-o", fn, "-b", "5b.pds"])
        
    def test03(self):
        fn = self.addTempFile("5c.sxw")
        pds2sxw.main(["-o", fn, "-b", "5c.pds"])

    def test04(self):
        fn = self.addTempFile("5d.sxc")
        pds2sxc.main(["-o", fn, "-b", "5d.pds"])

if __name__ == "__main__":
    tsttools.main()
