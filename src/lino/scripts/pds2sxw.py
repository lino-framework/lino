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

import sys, os

#from lino.ui import console
from lino.oogen import TextDocument

def pds2oo(docClass,argv):
    parser = console.getOptionParser(
        usage="usage: %prog [options] PDSFILE",
        description="""\
where PDSFILE is the pds file (oogen slang)
""" )
    
    parser.add_option("-o", "--output",
                      help="""\
generate to OUTFILE instead of default name. Default output filename
is PDSFILE with extension %s.
""" % docClass.extension,
                      action="store",
                      type="string",
                      dest="outFile",
                      default=None)
    
    (options, args) = parser.parse_args(argv)

    if len(args) != 1:
        parser.print_help() 
        return -1
    ifname = args[0]
    #print ifname
    (basename,ext) = os.path.splitext(ifname)
    #if ext != ".pds":
    #    ifname += ".pds"
    if options.outFile is None:
        filename = basename + docClass.extension
    else:
        filename = options.outFile
    doc = docClass(filename)
    job = console.job(ifname+" --> "+doc.filename)
    namespace = {'doc':doc}
    execfile(ifname,namespace,namespace)

    doc.save(console,showOutput=True)
    job.done()
    
##     if sys.platform == "win32" and console.isInteractive():
##         os.system("start %s" % g.outputFilename)
    
def main(argv):
    console.copyleft(name="Lino pds2sxw",
                     years='2004-2005')
    return pds2oo(TextDocument,argv)
    
        
if __name__ == '__main__':
    #g = main(sys.argv[1:])

    sys.exit(main(sys.argv[1:]))
