#----------------------------------------------------------------------
# makelc.py
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------
"""
create thumbnails and web-sized images if necessary
  
New naming scheme : the separate "thumbnails" tree used by publish is
replaced with the more "normal" method using "_tn" suffix.
  
"""

import os
import sys

from PIL import Image

from lino import copyleft
from lino.misc import console

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
						console.info("%s -> %s" % (pfn,tfn))
						im = Image.open(pfn)
						im.thumbnail(size.size) 
						im.save(tfn)
			
				

def main(argv):

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
    print copyleft(name="Lino/maketn",year='2002-2004')
    sys.exit(main(sys.argv[1:]))
    
