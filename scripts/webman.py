"""
WebMan creates static html files for one ore several WebMan modules.

A WebMan module is a directory containing a series `*.txt` files (with
reStructuredText content) and one file `init.wmi`. For each .txt file
will be written a .html file. The init.wmi is executed once per
module.

USAGE : lino webman [options] DIR1 [DIR2...]

OPTIONS:

-h, --help    show this help text
-f, --force   force generation even if target file is up-to-date
-b, --batch   batch processing : don't start webbrowser on result

"""


if __name__ == '__main__':
	import os,sys
	import getopt
	from lino import copyleft
	from lino.webman import __version__
	from lino.webman.static import wmm2html
	
	print copyleft('Lino/Webman', year='2003-2004')#,author='Luc Saffre')

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
