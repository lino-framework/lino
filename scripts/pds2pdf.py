"""\
Usage : pds2pdf [options] FILE

pds2pdf converts the Python Document Script FILE (extension `.pds`) to
a PDF file with same name, but `.pdf` as extension.
Extension `.pdf` will be added if not specified.
Note that you can specify only one FILE.

Options:
  
  -o NAME, --output NAME   alternate name for the output file
  -b, --batch              don't start Acrobat Reader on the generated pdf file
  -h, --help               display this text
"""

import sys, getopt, os
#from lino.timtools.pds2pdf import cli,__doc__
from lino.misc import gpl
from lino import __version__

from lino.sdoc.pdf import PdfRenderer
from lino.sdoc.pdsparser import main

if __name__ == '__main__':
	print "lino pds2pdf version " + __version__
	print gpl.copyright('2002-2003','Luc Saffre')

	try:
		opts, args = getopt.getopt(sys.argv[1:],
											"?ho:b",
											["help", "output=","batch"])

	except getopt.GetoptError,e:
		print __doc__
		print e
		sys.exit(-1)

	if len(args) != 1:
		print __doc__
		sys.exit(-1)

	outputfile = None
	showOutput = True
	
	for o, a in opts:
		if o in ("-?", "-h", "--help"):
			print __doc__
			sys.exit()
		elif o in ("-o", "--output"):
			outputfile = a
		elif o in ("-b", "--batch"):
			showOutput = False

	main(args[0],
		  PdfRenderer(),
		  outputfile,
		  showOutput=showOutput)
