## Copyright Luc Saffre 2003-2004.

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
testing textprinter
"""

import sys
import os

import win32ui
import win32con

from lino.misc import tsttools

class Case(tsttools.TestCase):
    ""

    def doit(self,d):
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
        
        d.endDoc()
        

    def test01(self):

        from lino.textprinter import winprn
        spoolFile = self.addTempFile("3.ps",showOutput=True)
        d = winprn.Win32PrinterDocument(self.win32_printerName_PS,
                                        spoolFile)
        self.doit(d)
        
    def test02(self):

        from lino.textprinter import pdfdoc
        fn = self.addTempFile("3.pdf",showOutput=True)
        d = pdfdoc.PdfDocument(fn)
        self.doit(d)
        
    def test03(self):

        from lino.textprinter import htmlprn
        fn = self.addTempFile("3.html",showOutput=True)
        f = open(fn,"wt")
        f.write("<html><body>")
        d = htmlprn.HTMLPrinterDocument(f)
        self.doit(d)
        f.write("</body></html>")
        f.close()

if __name__ == '__main__':
    tsttools.main()


