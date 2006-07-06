#encoding: cp850

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
import traceback

from lino.sdoc.pdf import PdfRenderer
from lino.sdoc.environment import ParseError
from lino.sdoc import commands

from lino.console.application import Application, UsageError

class Pds2pdf(Application):

    name="Lino/pds2pdf"

    copyright="""\
Copyright (c) 2002-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    url="http://lino.saffre-rumma.ee/pds2pdf.html"
    
    
    usage="usage: lino pds2pdf [options] FILE"
    description="""\
pds2pdf converts the Python Document Script FILE (extension `.pds`) to
a PDF file with same name, but `.pdf` as extension.
Extension `.pdf` will be added if not specified.
Note that you can specify only one FILE.
"""

    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)
    
        parser.add_option("-o", "--output",
                          help="""\
write to OUTFILE rather than FILE.pdf""",
                          action="store",
                          type="string",
                          dest="outFile",
                          default=None)
    


    def run(self):
        ofname=self.options.outFile
            
        if len(self.args) != 1:
            raise UsageError("needs 1 argument")

        ifname = self.args[0]

        (root,ext) = os.path.splitext(ifname)
        if ext == '':
            ifname += ".pds"

        if ofname is None:
            ofname = root 

        (head,tail) = os.path.split(ifname)
        initfile = os.path.join(head,'__init__.pds')

        namespace = {}
        namespace.update(globals())
        namespace['pds'] = commands

        renderer=PdfRenderer()

        try:
            commands.beginDocument(ofname,renderer,ifname)
            self.status(
                "%s --> %s...",
                commands.getSourceFileName(),
                commands.getOutputFileName())
            try:
                if os.path.exists(initfile):
                    execfile(initfile,namespace,namespace) 
                execfile(ifname,namespace,namespace)
                
                commands.endDocument(
                    showOutput=self.isInteractive())
                self.notice("%d pages." % commands.getPageNumber())
            except ParseError,e:
                raise
                #traceback.print_exc(2)
                # print document
                # print e
                # showOutput = False


        except IOError,e:
            print e
            return -1


#Pds2pdf().main()

## # lino.runscript expects a name consoleApplicationClass
## consoleApplicationClass = Pds2pdf

## if __name__ == '__main__':
##     consoleApplicationClass().main() # console,sys.argv[1:])
    


def main(*args,**kw):
    Pds2pdf().main(*args,**kw)

if __name__ == '__main__': main()
