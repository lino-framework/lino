## Copyright 2003-2005 Luc Saffre 

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
makelc renames all files in a tree to lower case.
Used to prepare a local (Windows) file tree for publishing to a
UNIX web server.
Works only on Windows (on UNIX it isn't necessary)

"""

import os
import sys

from lino.ui import console

class Collector:
    def __init__(self):
        self.dirnames = []
        self.filenames = []

    def __len__(self):
        return len(self.dirnames) + len(self.filenames)

def collect_upper(path,collector):
    
    """collect names of files or directories containing uppercase
     characters.  Returns a tuple of lists containing a tuple
     (orignial_name, lowercase_name) for each file to be processed. """
    for fn in os.listdir(path):
        pfn = os.path.join(path,fn)
        if os.path.isdir(pfn):
            if fn != fn.lower():
                collector.dirnames.append( (pfn, pfn.lower()))
            collect_upper(pfn,collector)
        else:
            if fn != fn.lower():
                i = (os.path.join(path.lower(),fn), pfn.lower())
                console.info( "%s -> %s" % i)
                collector.filenames.append(i)
                    
                


def main(argv):
    console.copyleft(name="Lino/makelc",years='2002-2005')
    parser = console.getOptionParser(
        usage="usage: %prog [options] DIR1 [DIR2 ...]",
        description="""\
where DIR1 DIR2... are the root directories to be
processed. Subdirectories of these directories will automatically be
processed.

""")

    (options, args) = parser.parse_args(argv)


    if len(args) == 0:
        parser.print_help() 
        return -1
    
    collector = Collector()
    
    for DIR in args:
        collect_upper(DIR,collector)
    
    if len(collector) > 0:
        if console.confirm( \
            "Okay to rename %d directories or files [Yn]?" % \
            len(collector)):
        
            for (o,n) in collector.filenames:
                os.rename(o,n)
            console.info("%d files renamed" % \
                             len(collector.filenames))

            for (o,n) in collector.dirnames:
                os.rename(o,n)
            console.info("%d directories renamed" % \
                             len(collector.dirnames))
    
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
        

	


