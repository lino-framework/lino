## Copyright 2006 Luc Saffre 

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

from lino.sdoc.pdf import PdfRenderer
from lino.sdoc.environment import ParseError
from lino.sdoc import commands

from lino.console.application import Application, UsageError

class PdfMake(Application):

    name="Lino/PdfMake"

    copyright="""\
Copyright (c) 2002-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    url="http://lino.saffre-rumma.ee/pdfmake.html"
    
    usage="usage: lino pdfmake [options] [FILE]"
    
    description="""\

PdfMake creates a PDF file named FILE and then runs Acrobat Reader to
view it. Default for FILE is "tmp.pdf".

"""

    

    def run(self,body,ofname=None):
        if ofname is None:
            if len(self.args) > 0:
                ofname=self.args[0]
            else:
                ofname="tmp.pdf"
            
        renderer=PdfRenderer()

        try:
            commands.beginDocument(ofname,renderer)
            self.status(
                "Writing %s...",commands.getOutputFileName())
            try:
                body()
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

