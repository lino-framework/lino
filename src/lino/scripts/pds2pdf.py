## Copyright 2004-2005 Luc Saffre

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


import sys, getopt, os
import traceback

from lino.ui import console

from lino.sdoc.pdf import PdfRenderer
from lino.sdoc.environment import ParseError
from lino.sdoc import commands


def pds2pdf(ifname,renderer,ofname=None, showOutput=True):

    (root,ext) = os.path.splitext(ifname)
    if ext == '':
        ifname += ".pds"

    if ofname is None:
        ofname = root 
        
    (head,tail) = os.path.split(ifname)
    initfile = os.path.join(head,'__init__.pds')

    try:
        commands.beginDocument(ofname,renderer,ifname)
        job = console.job(
            "%s --> %s..." % (commands.getSourceFileName(),
                              commands.getOutputFileName()))
        namespace = {}
        namespace.update(globals())
        namespace['pds'] = commands
        try:
            if os.path.exists(initfile):
                execfile(initfile,namespace,namespace) 
            execfile(ifname,namespace,namespace)
            commands.endDocument(showOutput)
            job.done("%d pages." % commands.getPageNumber())
        except ParseError,e:
            raise
            #traceback.print_exc(2)
            # print document
            # print e
            # showOutput = False


    except IOError,e:
        print e
        sys.exit(1)



def main(argv):
    console.copyleft(name="Lino/pds2pdf",
                     years='2002-2005',
                     author='Luc Saffre')

    parser = console.getOptionParser(
        usage="usage: lino pds2pdf [options] FILE",
        description="""\
pds2pdf converts the Python Document Script FILE (extension `.pds`) to
a PDF file with same name, but `.pdf` as extension.
Extension `.pdf` will be added if not specified.
Note that you can specify only one FILE.
""")

    
    parser.add_option("-o", "--output",
                      help="""\
write to OUTFILE rather than FILE.pdf""",
                      action="store",
                      type="string",
                      dest="outFile",
                      default=None)
    
    (options, args) = parser.parse_args(argv)

    if len(args) != 1:
        print args
        parser.print_help() 
        return -1
    
    inputfile = args[0]

    pds2pdf(inputfile,
         PdfRenderer(),
         options.outFile,
         showOutput=console.isInteractive())

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
    #main(sys.argv[1:])
