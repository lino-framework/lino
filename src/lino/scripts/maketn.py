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
create thumbnails and web-sized images if necessary
  
New naming scheme : the separate "thumbnails" tree used by publish is
replaced with the more "normal" method using "_tn" suffix.
  
"""

import os
import sys

from PIL import Image

from lino.ui import console

class Size:
	def __init__(self,suffix,size):
		self.suffix = "_" + suffix
		self.size = size


SIZES = [ #Size("tn",(128,128)),
    Size("web",(512,512)) ]

#EXTENSIONS = (".jpg",".png")
EXTENSIONS = (".jpg")

def make_tn(path,sizes):
	for fn in os.listdir(path):
		pfn = os.path.join(path,fn)
		if os.path.isdir(pfn):
			make_tn(pfn,sizes)
		else:
			(root,ext) = os.path.splitext(pfn)
			#(root,ext) = os.path.splitext(fn)
			if not ext in EXTENSIONS:
				continue
			for size in sizes:
				if root.endswith(size.suffix):
					# it's a thumbnail
					origname = root[:-len(size.suffix)]+ext
					if not os.path.exists(origname):
						print origname
						console.warning("Warning: original for %s does not exist" % pfn)
				else:
					#1 tfn = os.path.join(path,root) + size.suffix + ext
					tfn = root + size.suffix + ext
					# TODO : check whether it is older than original
					if not os.path.exists(tfn):
						console.verbose("%s -> %s" % (pfn,tfn))
						im = Image.open(pfn)
						im.thumbnail(size.size) 
						im.save(tfn)
			
				

def main(argv):

    console.copyleft(name="Lino/maketn",years='2002-2005')
    parser = console.getOptionParser(
        usage="usage: %prog [options] DIR1 [DIR2 ...]",
        description="""\
where DIR1 DIR2... are the root directories to be processed.
Subdirectories of these directories will automatically be
processed.

""")

    (options, args) = parser.parse_args(argv)


    if len(args) == 0:
        parser.print_help() 
        return -1
    
	for DIR in args:
		make_tn(DIR,SIZES)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
    
