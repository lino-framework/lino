raise Exception("makelower is replaced by makelc")

"""

prepares a webtim tree for publishing to a UNIX web server by renaming
all files and directories to lower case.

"""

from lino import copyleft

import os,sys

from lino.misc.console import confirm

VERBOSE=True
upperFilenames = []
upperDirnames = []

def collect_upper(path):
	for fn in os.listdir(path):
		pfn = os.path.join(path,fn)
		if os.path.isdir(pfn):
			if fn != fn.lower():
				upperDirnames.append( (pfn, pfn.lower()))
			collect_upper(pfn)
		else:
			if fn != fn.lower():
				i = (os.path.join(path.lower(),fn), pfn.lower())
				if VERBOSE:
					print "%s -> %s" % i # (pfn, pfn.lower())
				upperFilenames.append(i)

if __name__ == "__main__":

	print "Lino makelower"
	print copyleft(year='2002-2004')

	

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
		collect_upper(".")
	else:
		for root in args:
			collect_upper(root)

	if len(upperDirnames)+len(upperFilenames) == 0:
		if VERBOSE:
			print "Nothing to do"
			sys.exit()
			
	if confirm( "Okay to rename %d directories and %d files [Yn]?" %
					(len(upperDirnames),len(upperFilenames))):
		
		for (o,n) in upperDirnames:
			os.rename(o,n)
		if VERBOSE:
			print "%d directories renamed" % len(upperDirnames)

		for (o,n) in upperFilenames:
			os.rename(o,n)
		
		if VERBOSE:
			print "%d files renamed" % len(upperFilenames)


