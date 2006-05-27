#coding: latin1

## Copyright 2006 Luc Saffre.
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
import locale

from lino.console.application import Application, UsageError
from lino.reports.reports import DictReport
#from lino.gendoc.html import StaticHtmlDocument
from lino.gendoc.html import SimpleHtmlDocument as Document
from HyperText import HTML as html
#from HyperText.Documents import Document

def diag_encoding(doc):

    doc.header(2,"Some system settings related to encodings")
    
    s="    locale.getdefaultlocale(): "\
       + repr(locale.getdefaultlocale())

    s+="\n    sys.getdefaultencoding() : "+ sys.getdefaultencoding()
    s+="\n    sys.getfilesystemencoding() : " + sys.getfilesystemencoding()
    s+="\n    sys.stdout.encoding : "
    try:
        s+=str(sys.stdout.encoding)
    except AttributeError:
        s+=("(undefined)")
    s+="\n    sys.stdin.encoding : "
    try:
        s+=str(sys.stdin.encoding)
    except AttributeError:
        s+="(undefined)"
    s+="\n"
    doc.pre(s)

def diag_printer(doc):
    try:
        import win32print
    except ImportError,e:
        out.write("No module win32print (%s)\n" % e)
        return

    printerName=win32print.GetDefaultPrinter()
    doc.header(2,"Printer %s\n" % printerName)
    h=win32print.OpenPrinter(printerName)
    d=win32print.GetPrinter(h,2)
    devmode=d['pDevMode']
    ul=doc.ul()
    for n in dir(devmode):
        if n != 'DriverData' and n[0]!='_':
            ul.li("%r\t%r\n" % (n,getattr(devmode,n)))
    win32print.ClosePrinter(h)

class SysInfo(Application):
    name="Lino/SysInfo"
    copyright="""\
Copyright (c) 2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://lino.saffre-rumma.ee/sysinfo.html"
    
    usage="usage: lino countdown [options]"
    description="""\
writes some diagnostics about your computer.
""" 
    
    def run(self):
        if len(self.args) == 0:
            fp=self.toolkit.stdout
        elif len(self.args) == 1:
            fp=file(self.args[0])
        else:
            raise UsageError("Got more than 1 argument")

        doc=Document()
        #doc=StaticHtmlDocument()
        doc.header(1,"sysrpt")
        diag_encoding(doc)
        
        diag_printer(doc)
        
        doc.header(2,"sys.modules")
        doc.report(DictReport(sys.modules))
        
        #doc.save(self,targetRoot)
        doc.writeto(fp)
        



SysInfo().main()

        

