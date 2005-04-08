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

"""
testing textprinter.insertImage()
"""

from lino.misc.tsttools import TestCase, main
from lino.textprinter import winprn
from lino.textprinter import pdfprn
from lino.textprinter import htmlprn

class Case(TestCase):
    ""

    def doit(self,d):
        try:
            d.readfile(r"testdata\4.prn",coding="cp850")
        except Exception,e:
            print e
            #self.ui.error(str(e))
            
        d.endDoc()
        

    def test01(self):

        spoolFile = self.addTempFile("4.ps",showOutput=True)
        d = winprn.Win32TextPrinter(self.win32_printerName_PS,
                                    spoolFile)
        self.doit(d)
        
    def test02(self):
        return

        fn = self.addTempFile("3.pdf",showOutput=True)
        d = pdfprn.PdfTextPrinter(fn)
        self.doit(d)
        
    def test03(self):
        return
        fn = self.addTempFile("3.html",showOutput=True)
        f = open(fn,"wt")
        f.write("<html><body>")
        d = htmlprn.HtmlTextPrinter(f)
        self.doit(d)
        f.write("</body></html>")
        f.close()

if __name__ == '__main__':
    main()


