## Copyright 2006-2007 Luc Saffre 

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

import os
from lino.console.application import Application, UsageError
from lino import config

from lino.gendoc.pdf import PdfDocument
from lino.gendoc.html import HtmlDocument
#from lino.gendoc.plain import PlainDocument

def defaultbody(doc):
    doc.setTitle("Lino DocMaker")

    doc.memo("""

    Lino DocMaker is a another tool to generate documents.

    """)

class DocMaker(Application):

    name="Lino/DocMaker"

    copyright="""\
Copyright (c) 2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    url="http://lino.saffre-rumma.ee/docmaker.html"
    
    usage="usage: %s [options] [FILE]"
    
    description="""\

DocMaker generates a PDF or HTML file named FILE and (in interactive
mode) starts Acrobat Reader or the browser to view it.

"""

    default_output_file="tmp.pdf"

    def run(self,body=defaultbody,**kw):

        if len(self.args):
            filenames=self.args
        else:
            filenames=[self.default_output_file]
            
        for filename in filenames:
            if filename.endswith('.pdf'):
                doc=PdfDocument()
            elif filename.endswith('.html'):
                doc=HtmlDocument()
            else:
                raise UsageError("%s : unknown output file format")
            
            try:
                self.status("Preparing %s...",filename)
                body(doc)

                self.status("Writing %s...",filename)
                doc.saveas(filename,**kw)
                self.notice("%d pages." % doc.getPageNumber())
                self.showfile(filename)

            except IOError,e:
                print e
                return -1

