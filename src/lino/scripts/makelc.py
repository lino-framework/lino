#----------------------------------------------------------------------
# makelc.py
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------
"""
makelc prepares a local (Windows) file tree for publishing to a
(Linux) web server by renaming all files to lower case.

USAGE:  lino makelc [options] DIR [ DIR2 ... ]

where DIR and DIR2... are the root directories to be
processed. Subdirectories of these directories will automatically be
processed.

Options:

-b, --batch : don't ask confirmations
-q, --quiet : don't be verbose

Notes:
- This works only on Windows (on UNIX it isn't necessary)

"""

import os

from lino.misc.console import getSystemConsole

class Collector:
	def __init__(self):
		self.dirnames = []
		self.filenames = []

	def __len__(self):
		return len(self.dirnames) + len(self.filenames)

def collect_upper(path,console,collector):
	
	"""collect names of files or directories containing uppercase
	 characters.  Returns a tuple of lists containing a tuple
	 (orignial_name, lowercase_name) for each file to be processed. """
	for fn in os.listdir(path):
		pfn = os.path.join(path,fn)
		if os.path.isdir(pfn):
			if fn != fn.lower():
				collector.dirnames.append( (pfn, pfn.lower()))
			collect_upper(pfn,console,collector)
		else:
			if fn != fn.lower():
				i = (os.path.join(path.lower(),fn), pfn.lower())
				console.info( "%s -> %s" % i)
				collector.filenames.append(i)
					
				
def main(root,console=None,collector=None):
	if console is None:
		console = getSystemConsole()
	if collector is None:
		collector = Collector()
		
	collect_upper(root,console,collector)

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

	import sys
	from lino import copyleft
	
	print "Lino makelc"
	print copyleft(year='2002-2004')

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
		

	collector = Collector()
	
	for DIR in args:
		main(DIR,console,collector)

	


