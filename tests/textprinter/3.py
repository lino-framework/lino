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

        from lino.textprinter import winprn
        spoolFile = self.addTempFile("3.ps",showOutput=True)
        d = winprn.Win32PrinterDocument(self.win32_printerName_PS,
                                        spoolFile)
        d.printLine("")
        d.printLine("Win32PrinterDocument Test page")
        d.printLine("")
        cols = 9
        d.printLine("".join([" "*9+str(i+1) for i in range(cols)]))
        d.printLine("1234567890"*cols)
        d.printLine("")
        d.printLine("Here is some \x1bb1bold\x1bb0 text.")
        d.printLine("Here is some \x1bu1underlined\x1bu0 text.")
        d.printLine("Here is some \x1bi1italic\x1bi0 text.")
        
        d.endDoc()
        

if __name__ == '__main__':
    tsttools.main()


