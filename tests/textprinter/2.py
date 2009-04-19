## Copyright 2007-2009 Luc Saffre

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

This is another case where pdfprn and winprn produced different results.

"""

from lino.tools.tsttools import TestCase, main
#from lino import config

from lino.textprinter import winprn
from lino.textprinter import pdfprn

class Case(TestCase):
    ""

    def doit(self,d):
        INPUT="""\033c12
   This text is 12cpi
   \033c5 This text is 5cpi\033c12
   This text is again 12cpi """

        for line in INPUT.splitlines():
            d.writeln(line)
        d.close()
        

    def test01(self):

        spoolFile = self.addTempFile("2.ps",showOutput=True)
        d = winprn.Win32TextPrinter(
            #config.win32.get('postscript_printer'),
            self.runtests.options.postscript_printer,
            spoolFile)
        self.doit(d)
        
        spoolFile = self.addTempFile("2.pdf",showOutput=True)
        d = pdfprn.PdfTextPrinter(spoolFile)
        self.doit(d)
        

if __name__ == '__main__':
    main()


