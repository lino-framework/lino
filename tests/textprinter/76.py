## Copyright 2003-2009 Luc Saffre

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

"""
testing setPageLandscape()
"""

from lino.tools.tsttools import TestCase, main
#from lino import config

class Case(TestCase):
    ""

    def doit(self,d):
        d.setOrientationLandscape()
        d.drawDebugRaster()
        d.printLine("")
        d.printLine("Win32PrinterDocument Test page")
        d.printLine("")
        cols = 9
        d.printLine("".join([" "*9+str(i+1) for i in range(cols)]))
        d.printLine("1234567890"*cols)
        d.printLine("")
        d.printLine("Here is some \033b1bold\033b0 text.")
        d.printLine("Here is some \033u1underlined\033u0 text.")
        d.printLine("Here is some \033i1italic\033i0 text.")
        
        d.close()
        

    def test01(self):

        from lino.textprinter import winprn
        spoolFile = self.addTempFile("4.ps",showOutput=True)
        d = winprn.Win32TextPrinter(
            #config.win32.get('postscript_printer'),
            self.runtests.options.postscript_printer,
            spoolFile)
        self.doit(d)
        

if __name__ == '__main__':
    main()


