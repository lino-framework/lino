#coding: latin1

## Copyright 2004-2005 Luc Saffre 2004

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

from lino import copyleft
from lino.ui import console
from lino.textprinter import winprn 

def main(argv):

    parser = console.getOptionParser(
        usage="usage: %prog [options] FILE [FILE ...]",
        description="""\
where FILE is a plain text file to be printed on the Default Printer.
It must be in OEM charset and may contain simple formatting printer
control sequences, see http://lsaffre.dyndns.org/lino/prn2pdf.html
""" )
    
    parser.add_option("-p", "--printer",
                      help="""\
print on PRINTERNAME rather than on Default Printer.""",
                      action="store",
                      type="string",
                      dest="printerName",
                      default=None)
    
    parser.add_option("-o", "--output",
                      help="""\
write to SPOOLFILE rather than really printing.""",
                      action="store",
                      type="string",
                      dest="spoolFile",
                      default=None)
    
    (options, args) = parser.parse_args(argv)

    if len(args) == 0:
        parser.print_help() 
        sys.exit(-1)
    
    for inputfile in args:
        d = winprn.Win32PrinterDocument(options.printerName,
                                        options.spoolFile,
                                        charset=winprn.OEM_CHARSET)
        d.readfile(inputfile)
        d.endDoc()

    
        
if __name__ == '__main__':
    print copyleft(name="Lino/prn2print",
                   year='2004-2005')
    main(sys.argv[1:])
    
