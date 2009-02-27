## Copyright 2005-2009 Luc Saffre.
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

import sys

USAGE = """

Usage : lino runpy FILE

Executes the specified Python script FILE.
"""

def main():
    if len(sys.argv) <= 1:
        print USAGE
        sys.exit(-1)
        
    if sys.argv[1] == "--help":
        print USAGE
        sys.exit()
      
    filename=sys.argv[1]
    del sys.argv[1]
    execfile(filename,{})

if __name__ == '__main__': main()
