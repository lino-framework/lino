"""
WebMan creates static html files for one ore several WebMan modules.

A WebMan module is a directory containing a series `*.txt` files and
one file `init.py`.

(containing themselves text formatted using reStructuredText)

USAGE : lino webman [options] DIR1 DIR2

OPTIONS:

-h, --help    show this help text
-f, --force   force generation even if target file is up-to-date
-b, --batch   batch processing : don't start webbrowser on result

"""


if __name__ == '__main__':
	import os,sys
	import getopt
	from lino.misc import gpl
	from lino import __version__
	from lino.webman.static import wmm2html
	
	print "WebMan version " + __version__
	print gpl.copyright('2003','Luc Saffre')

	try:
		opts, args = getopt.getopt(sys.argv[1:],
											"h?bf",
											["help", "batch", "force"])

	except getopt.GetoptError:
		print __doc__
		sys.exit(-1)

	if len(args) != 1:
		print __doc__
		sys.exit(-1)

	showOutput=True
	force = False
	for o, a in opts:
		if o in ("-?", "-h", "--help"):
			print __doc__
			sys.exit()
		if o in ("-f", "--force"):
			force = True
		if o in ("-b", "--batch"):
			showOutput=False
		

	for srcdir in args: #sys.argv[1:]:
		wmm2html(srcdir,force=force,showOutput=showOutput)
