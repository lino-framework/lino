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

from lino import copyleft
from lino.sdoc.pdf import PdfRenderer
from lino.sdoc.environment import ParseError
from lino.sdoc import commands




def main(ifname,renderer,ofname=None,
         showOutput=True,
         verbose=True,
         force=True):

    (root,ext) = os.path.splitext(ifname)
    if ext == '':
        ifname += ".pds"

    if ofname is None:
        ofname = root 
        
    (head,tail) = os.path.split(ifname)
    initfile = os.path.join(head,'__init__.pds')

    try:
        commands.beginDocument(ofname,renderer,ifname)
        if verbose:
            print "%s --> %s..." % (commands.getSourceFileName(),
                                            commands.getOutputFileName())
        namespace = {}
        namespace.update(globals())
        namespace['pds'] = commands
        try:
            if os.path.exists(initfile):
                execfile(initfile,namespace,namespace) 
            execfile(ifname,namespace,namespace)
            commands.endDocument(showOutput)
            if verbose:
                print "%d pages." % commands.getPageNumber()
        except ParseError,e:
            raise
            #traceback.print_exc(2)
            # print document
            # print e
            # showOutput = False


    except IOError,e:
        print e
        sys.exit(1)



if __name__ == '__main__':
    print copyleft(name="Lino pds2pdf",
                   year='2002-2004',
                   author='Luc Saffre')

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                            "?ho:b",
                                            ["help", "output=","batch"])

    except getopt.GetoptError,e:
        print __doc__
        print e
        sys.exit(-1)

    if len(args) != 1:
        print __doc__
        sys.exit(-1)

    outputfile = None
    showOutput = True
    
    for o, a in opts:
        if o in ("-?", "-h", "--help"):
            print __doc__
            sys.exit()
        elif o in ("-o", "--output"):
            outputfile = a
        elif o in ("-b", "--batch"):
            showOutput = False

    main(args[0],
         PdfRenderer(),
         outputfile,
         showOutput=showOutput)
