## Copyright Luc Saffre 2003-2004.

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

"""lino webman [options] DIR [FILE1...]

Webman creates a static website from the files in DIR.

DIR should be a tree of directories containing .txt files (with
reStructuredText content) and/or *.jpg files, Optionally a file
`init.wmi` which is executed once per directory.

To process only some selected files, use FILE1... but this option is
currently ignored, Webman always processes all files.

"""

import os
import sys
import getopt

from lino import copyleft
from lino.ui import console
from lino.webman.static import wmm2html
    

def main(argv):

    parser = console.getOptionParser(
        usage=__doc__, #"usage: %prog [options] DIR",
        )
##         description="""\
## where DIR is the source directory.
## """)
    
    parser.add_option("-f", "--force",
                      help="""\
force generation even if target file is up-to-date""",
                      action="store_true",
                      dest="force",
                      default=False)
    
    parser.add_option("-d", "--dest",
                      help="""\
destination directory""",
                      action="store",
                      type="string",
                      dest="dest",
                      default=None)
    

    (options, args) = parser.parse_args(argv)


    if len(args) == 0:
        parser.print_help() 
        return -1
    
    wmm2html(srcdir=args[0],
             files=args[1:],
             outdir=options.dest,
             force=options.force
             )


if __name__ == '__main__':
    print copyleft(name="Lino/Webman", year='2003-2004')
    sys.exit(main(sys.argv[1:]))
    
