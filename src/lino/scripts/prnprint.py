#coding: iso-8859-1

## Copyright 2004-2006 Luc Saffre

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

import sys, os

#from lino.ui import console
from lino.textprinter import winprn
from lino.console.application import Application, UsageError

class PrnPrint(Application):
    
    name="Lino prnprint"
    copyright="""\
Copyright (c) 2004-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://lino.saffre-rumma.ee/prnprint.html"
    
    usage="usage: lino prnprint [options] FILE [FILE ...]"
    description="""\
where FILE is a plain text file to be printed on the Default Printer.
It must be in OEM charset and may contain simple formatting printer
control sequences, see http://lino.berlios.de/prn2pdf.html
""" 
    
    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)
    
        parser.add_option("-p", "--printer",
                          help="""\
print on PRINTERNAME rather than on Default Printer.""",
                          action="store",
                          type="string",
                          dest="printerName",
                          default=None)
    
        parser.add_option("-c", "--copies",
                          help="""\
print NUM copies.""",
                          action="store",
                          type="int",
                          dest="copies",
                          default=1)
    
        parser.add_option("-o", "--output",
                          help="""\
write to SPOOLFILE rather than really printing.""",
                          action="store",
                          type="string",
                          dest="spoolFile",
                          default=None)
        
        parser.add_option(
            "-u", "--useWorldTransform",
            help="use SetWorldTransform() to implement landscape",
            action="store_true",
            dest="useWorldTransform",
            default=False)
    
    def run(self):
        if len(self.args) == 0:
            raise UsageError("no arguments specified")
        if self.options.copies < 0:
            raise UsageError("wrong value for --copies")
        if self.options.printerName is not None:
            self.notice("Printing on printer '%s'",
                        self.options.printerName)
        for inputfile in self.args:
            for cp in range(self.options.copies):
                d = winprn.Win32TextPrinter(self,
                    self.options.printerName,
                    self.options.spoolFile,
                    useWorldTransform=self.options.useWorldTransform,
                    coding=sys.stdin.encoding)
                    #charset=winprn.OEM_CHARSET)
                d.readfile(inputfile)
                d.endDoc()
                if d.page == 1:
                    self.notice("%s : 1 page has been printed",
                                inputfile)
                else:
                    self.notice("%s : %d pages have been printed",
                                inputfile,d.page)


## consoleApplicationClass = PrnPrint

# PrnPrint().main()
    
        
## if __name__ == '__main__':
##    PrnPrint().main()
##     consoleApplicationClass().main() # console,sys.argv[1:])
    
def main(*args,**kw):
    PrnPrint().main(*args,**kw)
