raise "not used"

import os,sys

from docutils import core
from lino.webman.xdocutils import Writer

"""
Note:
html in a separate directory tree : advantage : one keystroke
less in Emacs when opening a file. Disadvantages: cleanup
problem. Some non-generated files (`.cvsignore`, `lino.css`, pictures)
are mixed-up between the generated html files.			 
"""

DEFAULTS = {'input_encoding': 'latin-1',
				'output_encoding': 'latin-1',
				'stylesheet_path': 'default.css',
				'source_link': 1,
				'tab_width': 3,
				'datestamp' : '%Y-%m-%d %H:%M UTC',
				'generator': 1 
				}


def txt2html(source_path=None,destination_path=None,argv=None):
	description = ('Generates HTML from RST files using expansion.	 '
						+ core.default_description)

	pub = core.Publisher(writer=Writer())
	pub.set_components('standalone', 'restructuredtext', None)
	pub.process_command_line(argv,
									 description=description,
									 **DEFAULTS)
	if source_path:
		pub.set_source(None, source_path)
	if destination_path:
		pub.set_destination(None, destination_path)
	pub.publish() #enable_exit=enable_exit)




def dir_txt2html(sourceRoot,localRoot=None):
	sourceRoot = os.path.abspath(sourceRoot)
	if localRoot is None:
		localRoot = sourceRoot
	cwd = os.getcwd()
	os.chdir(sourceRoot)
	for root, dirs, files in os.walk('.'):
		#print "localRoot=%s" % localRoot
		#print "root=%s" % root
		outDir = os.path.normpath(os.path.join(localRoot,root))
		#print "outDir=%s" % outDir
		if not os.path.exists(outDir):
			os.makedirs(outDir)
		os.chdir(outDir)
		#print os.getcwd()
		for fn in files:
			(base,ext) = os.path.splitext(fn)
			if ext == '.txt':
				outfile = os.path.join(outDir,base)+'.html'
				updodate = False
				try:
					if os.path.getmtime(outfile) > os.path.getmtime(fn):
						updodate = True
				except os.error:
					pass
				if updodate:
					print "%s : up to date" % outfile
				else:
					print "Processing %s..." % outfile
					if True:	# new processing since 2003-11-12
						txt2html(fn,outfile)
					else:
						body = open(fn).read()
						try:
							body = em.expand(body,globals())
							# print body
							settings = {'input_encoding': 'latin-1',
											'output_encoding': 'latin-1',
											'stylesheet_path': 'lino.css',
											'source_link': 1,
											'datestamp' : '%Y-%m-%d %H:%M UTC',
											'generator': 1 
											}
							body = core.publish_string(
								body,
								writer_name='html',
								settings_overrides=settings)
							open(outfile,"w").write(body)
						except:
							pass
		os.chdir(sourceRoot)

	os.chdir(cwd)

## def cli():
## 	from lino.misc import gpl
## 	from lino.version import __version__
## 	print "txt2html version " + __version__
## 	print gpl.copyright('2003','Luc Saffre')
## 	for sourceRoot in sys.argv[1:]:
## 		txt2html(sourceRoot)

def cli():
	from lino.misc import gpl
	from lino import __version__
	print "txt2html version " + __version__
	print gpl.copyright('2003','Luc Saffre')
	srcpath=sys.argv[1]
	if srcpath.endswith('.txt'):
		destpath = srcpath[:-4] + ".html"
	else:
		destpath = srcpath + ".html"
		srcpath += ".txt"
	msg = "%s -> %s" % (srcpath,destpath)
	print msg
	#from lino.misc.console import confirm
	#if confirm(msg):
	txt2html(srcpath,destpath,sys.argv[2:])
## 	for sourceRoot in sys.argv[1:]:
## 		publish_file(source_path=fn,
## 						 destination_path=outfile)

if __name__ == "__main__":
	cli()


