## Copyright Luc Saffre 2004-2005.

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
from lino.oogen import Document,OoText,OoSpreadsheet

def main(argv):

    parser = console.getOptionParser(
        usage="usage: %prog [options] PDSFILE",
        description="""\
where PDSFILE is the pds file (oogen slang)
""" )
    
    parser.add_option("-c", "--component",
                      help="""\
.""",
                      action="store",
                      type="string",
                      dest="component",
                      default=None)
    
    parser.add_option("-o", "--output",
                      help="""\
output to specified instead of default name.""",
                      action="store",
                      type="string",
                      dest="outputFile",
                      default=None)
    
    (options, args) = parser.parse_args(argv)

    if len(args) == 0:
        parser.print_help() 
        sys.exit(-1)
    
    for ifname in args:
        (basename,ext) = os.path.splitext(ifname)
        if ext != ".pds":
            ifname += ".pds"
        console.progress("Processing " +ifname+" ...")
        doc = Document(basename)
        namespace = {'doc':doc}
        try:
            execfile(ifname,namespace,namespace)
        except ParseError,e:
            raise
        doc.generate()

    
        
if __name__ == '__main__':
    print copyleft(name="Lino/oogen", year='2004-2005')
    main(sys.argv[1:])
    
