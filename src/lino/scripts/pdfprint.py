# -*- coding: iso-8859-1 -*-

## Copyright 2004-2009 Luc Saffre

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
import win32api

from lino.textprinter import winprn
from lino.console.application import Application, UsageError


class PdfPrint(Application):
    
    name="Lino pdfprint"
    copyright="""\
Copyright (c) 2009 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://lino.saffre-rumma.ee/pdfprint.html"
    
    usage="usage: lino pdfprint [options] FILE [FILE ...]"
    description="""

where FILE is a PDF file to be printed directly on your Windows
Printer.

Thanks to Thomas Blatter who posted the method:
http://two.pairlist.net/pipermail/reportlab-users/2005-May/003936.html

""" 
    configfile="pdfprint.ini" 
    
        
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
    
    
    def run(self):
        if len(self.args) == 0:
            raise UsageError("no arguments specified")
        if self.options.printerName is not None:
            raise UsageError("Sorry, pdfprint currently can print only to the standard printer")
        if self.options.copies < 0:
            raise UsageError("wrong value for --copies")
            
            
        for inputfile in self.args:
            for cp in range(self.options.copies):
                win32api.ShellExecute(0,"print",inputfile,None,".",0)
                name=self.options.printerName
                if name is None:
                    name="Standard Printer"
                self.notice("%s has been printed on %s",
                            inputfile,name)


def main(*args,**kw):
    PdfPrint().main(*args,**kw)

if __name__ == '__main__':
    main()
