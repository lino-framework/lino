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

from lino.ui import console
from lino.textprinter.winprn import Win32PrinterDocument
from lino.textprinter.pdfdoc import PdfDocument

def doit(d):
    d.writeln("")
    d.writeln("lino.textprinter Test page")
    d.writeln("")
    cols = int(d.getWidth() / 10) + 1
    d.writeln("".join([" "*9+str(i+1) for i in range(cols)]))
    d.writeln("1234567890"*cols)
    d.writeln("")
    d.writeln("Here is some \033b1bold\033b0 text.")
    d.writeln("Here is some \033u1underlined\033u0 text.")
    d.writeln("Here is some \033i1italic\033i0 text.")
    d.endDoc()
        

def main():
    
    # first on console:
    d = console.textprinter()
    doit(d)
    
    # now on the printer:
    if console.confirm(
        "print it on your default Windows printer?"):
        d = Win32PrinterDocument()
        doit(d)
        
    # and now on a PDF document:
    filename = "test.pdf"
    if console.confirm("start Acrobat Reader on %s?" % filename):
        d = PdfDocument(filename)
        doit(d)
        os.system("start "+filename)
        
if __name__ == '__main__':
    main()


