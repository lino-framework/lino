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

"""
prn2pdf converts a file containing text and simple formatting
printer control sequences into a PDF file.  

USAGE :
  prn2pdf [options] FILE

  where FILE is the .prn file to be converted 
  
OPTIONS :
  -o, --output FILE     write result to file FILE
  -b, --batch           don't start Acrobat Reader on the generated
                        pdf file
  -h, --help            display this text

"""

import sys, os

from lino.ui import console 
from lino.textprinter.pdfdoc import PdfDocument


def main(argv):
    console.copyleft(name="Lino/prn2pdf",
                     years='2002-2005',
                     author='Luc Saffre')
    
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
        print args
        parser.print_help() 
        sys.exit(-1)
    
    inputfile = args[0]
    (root,ext) = os.path.splitext(inputfile)
    if options.outFile is None:
        options.outFile = root +".pdf"
    d = PdfDocument(options.outFile)#, coding="cp850")
    #d.readfile(inputfile,coding="cp850")
    d.readfile(inputfile,coding=sys.stdin.encoding)
    d.endDoc()
    if sys.platform == "win32" and console.isInteractive():
        os.system("start %s" % options.outFile)

    




if __name__ == '__main__':
    main(sys.argv[1:])

