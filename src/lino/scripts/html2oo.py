## Copyright Luc Saffre 2005

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
from htmllib import HTMLParser
import  formatter

from lino.ui import console
from lino.oogen import Document


class MyParser(HTMLParser):

    def __init__(self, formatter, verbose=0):
        HTMLParser.__init__(self, formatter, verbose)
        self._tableStack = []
        self._currentTable = None
        self._currentCell = None
        self._tablesFound =[]


    
    def unknown_starttag(self, tag, attrs):
        if tag == "table":
            t = []
            self._tableStack.append(t)
            self._currentTable = t
            self._currentRow = None
            self._currentCell = None
        elif tag == "tr":
            r = []
            self._currentTable.append(r)
            self._currentRow = r
            self._currentCell = None
        elif tag == "td":
            c = ""
            self._currentRow.append(c)
            self._currentCell = c

    def unknown_endtag(self, tag):
        if tag == "table":
            t = self._tableStack.pop()
            self._tablesFound.append(t)
            if len(self._tableStack):
                self._currentTable = self._tableStack[-1]
                self._currentRow = self._currentTable[-1]
                self._currentCell = self._currentRow[-1]
            else:
                self._currentTable = None
                self._currentRow = None
                self._currentCell = None
        elif tag == "tr":
            self._currentRow = None
            self._currentCell = None
        elif tag == "td":
            self._currentRow.append(self._currentCell)
            self._currentCell = None

    def handle_data(self, data):
        if self._currentCell is None:
            pass
        else:
            self._currentCell += data

## def main(args):            
##     w = formatter.NullWriter()
##     fmt = formatter.AbstractFormatter(w)
##     parser = MyParser(fmt)
##     parser.feed(open('maksuamet-2004.htm').read())
##     parser.close()
##     print "%d tables found" % len(parser._tablesFound)
##     for i in range(len(parser._tablesFound)):
##         t = parser._tablesFound[i]
##         print "table %s has %d rows" % (i,len(t))



def main(argv):
    console.copyleft(name="Lino/html2sxc", years='2005')
    parser = console.getOptionParser(
        usage="usage: %prog [options] HTMLFILE",
        description="""\
where HTMLFILE is a html document containg tables
""" )
    
    parser.add_option("-o", "--output",
                      help="""\
generate to OUTFILE instead of default name. Default output filename
is HTMLFILE with extension .sxc depending on content.
""",
                      action="store",
                      type="string",
                      dest="outFile",
                      default=None)
    
    (options, args) = parser.parse_args(argv)

    if len(args) != 1:
        parser.print_help() 
        sys.exit(-1)
    ifname = args[0]
    print ifname
    (basename,ext) = os.path.splitext(ifname)
    console.progress("Processing " +ifname+" ...")
    doc = Document(basename+".sxc")

    w = formatter.NullWriter()
    fmt = formatter.AbstractFormatter(w)
    parser = MyParser(fmt)
    parser.feed(open(ifname).read())
    parser.close()
    for t in parser._tablesFound:
        dt = doc.table()
        for r in t:
            dt.addRow(*r)
    g=doc.generator(filename=options.outFile)
    g.save()
    if sys.platform == "win32" and console.isInteractive():
        os.system("start %s" % g.outputFilename)
    
    
        

if __name__ == "__main__":
    main(sys.argv[1:])
