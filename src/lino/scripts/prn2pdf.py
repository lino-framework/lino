#coding: latin1

## Copyright 2002-2005 Luc Saffre.

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

from lino.ui import console 
from lino.textprinter.pdfprn import PdfTextPrinter


def main(argv):
    parser = console.getOptionParser(
        usage="usage: lino prn2pdf [options] FILE",
        description="""\
where FILE is the file to be converted to a pdf file.
It may contain plain text and simple formatting printer control sequences. """ )
    
    parser.add_option("-o", "--output",
                      help="""\
write to OUTFILE rather than FILE.pdf""",
                      action="store",
                      type="string",
                      dest="outFile",
                      default=None)
    
    (options, args) = parser.parse_args(argv)

    if len(args) != 1:
        #print args
        parser.print_help() 
        return -1
    
    inputfile = args[0]
    if options.outFile is None:
        (root,ext) = os.path.splitext(inputfile)
        options.outFile = root +".pdf"
    d = PdfTextPrinter(options.outFile)
    ok = True
    try:
        d.readfile(inputfile,coding=sys.stdin.encoding)
    except Exception,e:
        console.error(str(e))
        ok = False
    
    d.endDoc()
    if not ok:
        return -1
    
    if sys.platform == "win32" and console.isInteractive():
        os.system("start %s" % options.outFile)

    




if __name__ == '__main__':
    console.copyleft(name="Lino/prn2pdf",
                     years='2002-2005',
                     author='Luc Saffre')
    
    sys.exit(main(sys.argv[1:]))

