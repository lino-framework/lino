#----------------------------------------------------------------------
# makelc.py
# Copyright: (c) 2003-2004 Luc Saffre
# License:   GPL
#----------------------------------------------------------------------
"""
makelc renames all files in a tree to lower case.
Used to prepare a local (Windows) file tree for publishing to a
UNIX web server.
Works only on Windows (on UNIX it isn't necessary)

"""

import os
import sys

from lino import copyleft
from lino.misc import console

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
    print copyleft(name="Lino/makelc",year='2002-2004')
    sys.exit(main(sys.argv[1:]))
        

	


