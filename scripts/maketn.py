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

from PIL import Image

from lino.misc.console import getSystemConsole

class Size:
	def __init__(self,suffix,size):
		self.suffix = "_" + suffix
		self.size = size


SIZES = [ #Size("tn",(128,128)),
			 Size("web",(512,512)) ]

#EXTENSIONS = (".jpg",".png")
EXTENSIONS = (".jpg")

def make_tn(path,sizes,console):
	for fn in os.listdir(path):
		pfn = os.path.join(path,fn)
		if os.path.isdir(pfn):
			make_tn(pfn,sizes,console)
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
			
				


if __name__ == "__main__":
	import sys
	from lino import copyleft
	
	print "Lino maketn"
	print copyleft(year='2002-2004',author='Luc Saffre')
	

	import getopt
	try:
		opts, args = getopt.getopt(sys.argv[1:],
											"h?qb",
											["help", "quiet", "batch"])

	except getopt.GetoptError:
		print __doc__
		sys.exit(-1)


	if len(args) == 0:
		print __doc__
		sys.exit(-1)

	console = getSystemConsole(verbose=True,batch=False,debug=False)

	for o, a in opts:
		if o in ("-?", "-h", "--help"):
			print __doc__
			sys.exit()
		if o in ("-q", "--quiet"):
			console.set(verbose=False)
		if o in ("-b", "--batch"):
			console.set(batch=True)
		

	for DIR in args:
		make_tn(DIR,SIZES,console)
