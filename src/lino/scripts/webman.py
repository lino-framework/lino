#----------------------------------------------------------------------
# Copyright 2003-2004 Luc Saffre
# This file is published as part of the Lino project
#----------------------------------------------------------------------
"""
Webman creates static html files for a Webman site.

A Webman site is a directory containing a series .txt files (with
reStructuredText content) and one file `init.wmi`. For each .txt file
will be written a .html file. The init.wmi is executed once per
module.

USAGE : lino webman [options] DIR1 [DIR2...]

OPTIONS:

-h, --help    show this help text
-f, --force   force generation even if target file is up-to-date
-b, --batch   batch processing : don't start webbrowser on result

"""

import os
import sys
import getopt

from lino import copyleft
from lino.misc import console
from lino.webman.static import wmm2html
    

def main(argv):

    parser = console.getOptionParser(
        usage="usage: %prog [options] DIR",
        description="""\
where DIR is the source directory.
""")
    
    parser.add_option("-f", "--force",
                      help="""\
force generation even if target file is up-to-date""",
                      action="store",
                      type="string",
                      dest="force",
                      default=False)
    
    parser.add_option("-d", "--dest",
                      help="""\
destination dir root""",
                      action="store",
                      type="string",
                      dest="dest",
                      default=None)
    

    (options, args) = parser.parse_args(argv)


    if len(args) == 0:
        parser.print_help() 
        return -1
    
    for srcdir in args: 
        wmm2html(srcdir,
                 outdir=options.dest,
                 force=options.force
                 )


if __name__ == '__main__':
    print copyleft(name="Lino/Webman", year='2003-2004')
    sys.exit(main(sys.argv[1:]))
    
