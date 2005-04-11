#coding: latin1
"""
testing textprinter.insertImage()
"""

from lino.misc.tsttools import TestCase, main
from lino.textprinter import winprn
from lino.ui import console


def main():
    spoolFile = r"tmp.ps"
    d = winprn.Win32TextPrinter("Lexmark Optra PS",
                                spoolFile,
                                coding="cp850")
    d.writeln("--- File 2a.prn:---")
    d.readfile("2a.prn",coding="cp850")
    d.writeln("--- eof 2a.prn---")
    
    d.writeln("--- File 2b.prn:---")
    d.readfile("2b.prn",coding="cp850")
    d.writeln("--- eof 2b.prn---")
    
    d.writeln("Here is some more text.")
    d.writeln("Ännchen Müller machte große Augen.")
    d.write("And here")
    d.write(" is some")
    d.write(" frag")
    d.writeln("mented text.")
    d.drawDebugRaster()
    d.endDoc()
        
        
if __name__ == '__main__':
    console.parse_args()
    main()


