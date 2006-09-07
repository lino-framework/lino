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

"""
testing textprinter
"""

from lino.misc.tsttools import TestCase, main

class Case(TestCase):
    ""

    def doit(self,d):
        d.printLine("")
        d.printLine("TextPrinter Test page")
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
        spoolFile = self.addTempFile("3.ps",showOutput=True)
        d = winprn.Win32TextPrinter(self.win32_printerName_PS,
                                    spoolFile)
        self.doit(d)
        
    def test02(self):

        from lino.textprinter import pdfprn
        fn = self.addTempFile("3.pdf",showOutput=True)
        d = pdfprn.PdfTextPrinter(fn)
        self.doit(d)
        
    def test03(self):

        from lino.textprinter import htmlprn
        fn = self.addTempFile("3.html",showOutput=True)
        #f = open(fn,"wt")
        #f.write("<html><body>")
        d = htmlprn.HtmlTextPrinter(fn)
        self.doit(d)
        #f.write("</body></html>")
        #f.close()
        
    def test04(self):

        from lino.textprinter import plain
        d = plain.PlainTextPrinter()
        self.doit(d)
        s=self.getConsoleOutput()
        self.assertEquivalent(s,"""
+------------------------------------------------------------------------+
|                                                                        |
|TextPrinter Test page                                                   |
|                                                                        |
|         1         2         3         4         5         6         7  |
|123456789012345678901234567890123456789012345678901234567890123456789012|
|                                                                        |
|Here is some bold text.                                                 |
|Here is some underlined text.                                           |
|Here is some italic text.                                               |
+------------------------------------------------------------------------+        
        """)
        

if __name__ == '__main__':
    main()


