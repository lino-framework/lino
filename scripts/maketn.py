"""
create thumbnails if necessary
  
New naming scheme : the separate "thumbnails" tree used by publish is
replaced with the more "normal" method using "_tn" suffix.

  
  
"""

import os,sys

from PIL import Image

class Size:
	def __init__(self,suffix,size):
		self.suffix = "_" + suffix
		self.size = size


SIZES = [ #Size("tn",(128,128)),
			 Size("web",(512,512)) ]

EXTENSIONS = (".jpg",".png")
VERBOSE = True

def make_tn(path,sizes=SIZES):
	for fn in os.listdir(path):
		pfn = os.path.join(path,fn)
		if os.path.isdir(pfn):
			make_tn(pfn,sizes)
		else:
			(root,ext) = os.path.splitext(fn)
			if not ext in EXTENSIONS:
				continue
			for size in sizes:
				if root.endswith(size.suffix):
					# it's a thumbnail
					origname = root[:-len(size.suffix)]+ext
					if not os.path.exist(origname):
						print origname
						print "Warning: original for %s does not exist" % pfn
				else:
					tfn = os.path.join(path,root) + size.suffix + ext
					# TODO : check whether it is older than original
					if not os.path.exists(tfn):
						if VERBOSE:
							print "%s -> %s" % (pfn,tfn)
						im = Image.open(pfn)
						im.thumbnail(size.size) 
						im.save(tfn)
			
				
if __name__ == "__main__":
	from lino import copyright
	
	print "Lino makethumbs"
	print copyright('2002-2004','Luc Saffre')
	

	import getopt
	try:
		opts, args = getopt.getopt(sys.argv[1:],
											"h?q",
											["help", "quiet"])

	except getopt.GetoptError:
		print __doc__
		sys.exit(-1)

	for o, a in opts:
		if o in ("-?", "-h", "--help"):
			print __doc__
			sys.exit()
		if o in ("-q", "--quiet"):
			VERBOSE=False
		

	if len(args) == 0:
		make_tn(".")
	else:
		for jpgdir in args:
			make_tn(jpgdir)
