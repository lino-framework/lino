import os,sys

from docutils import core
from lino.webman.webman import WebModule
from lino.misc.console import confirm

## DEFAULTS = {'input_encoding': 'latin-1',
## 				'output_encoding': 'latin-1',
## 				'stylesheet_path': 'default.css',
## 				'source_link': 1,
## 				'tab_width': 3,
## 				'datestamp' : '%Y-%m-%d %H:%M UTC',
## 				'generator': 1 
## 				}


def _wmm2html(webmod,outdir=None,force=False):

	if not os.path.exists(outdir):
		os.makedirs(outdir)
		
	for (name,page) in webmod._pages.items():
		if isinstance(page,WebModule):
			_wmm2html(page,os.path.join(outdir,name),force)
		else:
			outfile = os.path.join(outdir,name)+'.html'
			srcfile = page.getSourcePath()
			updodate = False
			if not force:
				try:
					if os.path.getmtime(outfile) > os.path.getmtime(srcfile):
						updodate = True
				except os.error:
					pass
			if updodate:
				print "%s : up to date" % outfile
			else:
				print "Processing %s..." % outfile
				html = page(request=None)
				open(outfile,"w").write(html)

def wmm2html(srcdir,outdir=None,force=False,showOutput=True):
	"""convert a complete module to static html
	"""
	#
	if outdir is None:
		outdir = srcdir

	webmod = WebModule(srcdir)

	_wmm2html(webmod,outdir,force)

	#outDir = os.path.normpath(os.path.join(localRoot,root))
		#print "outDir=%s" % outDir
			
	#os.chdir(cwd)

	if showOutput:
		import webbrowser
		webbrowser.open(os.path.join(outdir,'index.html'),new=True)

