#coding:latin1
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

import sys
import os
opj=os.path.join
from lino.misc.tsttools import TestCase, main

dataPath = os.path.join(os.path.dirname(__file__),
                        'testdata','textprinter')
dataPath = os.path.abspath(dataPath)

class Case(TestCase):
    ""

    def doit(self,d):

        d.writeln("--- File 5.prn:---")
        d.readfile(opj(dataPath,"5.prn"),coding="cp850")
        d.writeln("--- eof 5.prn---")

        d.writeln("Here is some more text.")
        d.writeln(u"Ännchen Müller machte große Augen.")
        d.write("And here")
        d.write(" is some")
        d.write(" frag")
        d.writeln("mented text.")
        #d.drawDebugRaster()
        d.endDoc()
        

    def test01(self):

        from lino.textprinter import winprn
        spoolFile = self.addTempFile("5.ps",showOutput=True)
        d = winprn.Win32TextPrinter(self.win32_printerName_PS,
                                    spoolFile )
        self.doit(d)
        

if __name__ == '__main__':
    main()


