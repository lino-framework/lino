# coding: latin1
#----------------------------------------------------------------------
# Copyright: (c) 2003-2004 Luc Saffre
# License:   GPL
#----------------------------------------------------------------------

"""
testing prnprinter
"""

import sys
import os

import win32ui
import win32con

from lino.misc import tsttools

class Case(tsttools.TestCase):
    ""

    def test01(self):
        spoolFile = self.addTempFile("2.ps",showOutput=True)
        dc = win32ui.CreateDC()
        dc.CreatePrinterDC(self.win32_printerName_PS)
        dc.StartDoc("my print job",spoolFile)
        dc.SetMapMode(win32con.MM_TWIPS)
        dc.StartPage()
        minx, miny = dc.GetWindowOrg()
        maxx,maxy = dc.GetWindowExt()
        for x in range(minx,maxx,1440):
            for y in range(-miny,-maxy,-1440):
                dc.TextOut(x,y,repr((x,y)))
        dc.EndDoc()



if __name__ == '__main__':
    tsttools.main()

