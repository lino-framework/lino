## Copyright Luc Saffre 2004.

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


"""\
Usage : pds2pdf [options] FILE

pds2pdf converts the Python Document Script FILE (extension `.pds`) to
a PDF file with same name, but `.pdf` as extension.
Extension `.pdf` will be added if not specified.
Note that you can specify only one FILE.

Options:
  
  -h, --help               display this text
  -o NAME, --output NAME   alternate name for the output file
  -b, --batch              don't start Acrobat Reader on the
                           generated pdf file
                           
"""

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
        sys.exit(-1)
    
    inputfile = args[0]


    

##     try:
##         opts, args = getopt.getopt(argv,
##                                    "?ho:b",
##                                    ["help", "output=","batch"])

##     except getopt.GetoptError,e:
##         print __doc__
##         print e
##         sys.exit(-1)

##     if len(args) != 1:
##         print __doc__
##         sys.exit(-1)

##     outputfile = None
##     showOutput = True
    
##     for o, a in opts:
##         if o in ("-?", "-h", "--help"):
##             print __doc__
##             sys.exit()
##         elif o in ("-o", "--output"):
##             outputfile = a
##         elif o in ("-b", "--batch"):
##             showOutput = False

    pds2pdf(inputfile,
         PdfRenderer(),
         options.outFile,
         showOutput=console.isInteractive())

if __name__ == '__main__':
    main(sys.argv[1:])
