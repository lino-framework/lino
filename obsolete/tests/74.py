## Copyright 2003-2006 Luc Saffre

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

import win32ui
import win32con

from lino.misc import tsttools
from lino import config

class Case(tsttools.TestCase):
    ""

    def test01(self):
        spoolFile = self.addTempFile("74.ps",showOutput=True)
        dc = win32ui.CreateDC()
        dc.CreatePrinterDC(config.win32.get('postscript_printer'))
        dc.StartDoc("my print job",spoolFile)
        dc.SetMapMode(win32con.MM_TWIPS)
        dc.StartPage()
        minx, miny = dc.GetWindowOrg()
        maxx,maxy = dc.GetWindowExt()
        for x in range(minx,maxx,1440):
            for y in range(miny,maxy,1440):
                dc.TextOut(x,-y,repr((x,y)))
        dc.EndDoc()



if __name__ == '__main__':
    tsttools.main()

