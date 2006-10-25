#coding:latin1
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

import sys
import os
opj=os.path.join
from lino.misc.tsttools import TestCase, main
from lino.textprinter import winprn
from lino import config

dataPath = os.path.join(
    config.paths.get('docs_path'),'examples','textprinter')

class Case(TestCase):
    ""

    def doit(self,d):

        d.writeln("--- File 5.prn:---")
        d.readfile(opj(dataPath,"5.prn"),encoding="cp850")
        d.writeln("--- eof 5.prn---")

        d.writeln("Here is some more text.")
        d.writeln(u"Ännchen Müller machte große Augen.")
        d.write("And here")
        d.write(" is some")
        d.write(" frag")
        d.writeln("mented text.")

        d.writeln()
        d.write("This is a very long line. ")
        d.write("Just do demonstrate that TextPrinter ")
        d.write("doesn't wrap paragraphs for you...")
        d.write("Blabla bla. "*20)
        d.writeln("Amen.")
        
        #d.drawDebugRaster()
        d.close()
        

    def test01(self):

        spoolFile = self.addTempFile("77.ps",showOutput=True)
        d = winprn.Win32TextPrinter(
            config.win32.get('postscript_printer'),spoolFile )
        self.doit(d)

        
        spoolFile = self.addTempFile("77L.ps",showOutput=True)
        d = winprn.Win32TextPrinter(
            config.win32.get('postscript_printer'),spoolFile )
        d.setOrientationLandscape()
        d.writeln("And now the same in landscape. ")
        d.writeln()
        self.doit(d)
        

if __name__ == '__main__':
    main()


