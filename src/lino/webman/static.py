import os,sys

from docutils import core
from lino.webman.nodes import Site, WebModule, TxtWebPage
from lino.misc.console import confirm

## DEFAULTS = {'input_encoding': 'latin-1',
## 				'output_encoding': 'latin-1',
## 				'stylesheet_path': 'default.css',
## 				'source_link': 1,
## 				'tab_width': 3,
## 				'datestamp' : '%Y-%m-%d %H:%M UTC',
## 				'generator': 1 
## 				}


def _wmm2html(node,force=False):

	#outfile = os.path.join(outdir,node.name)+'.html'
	outfile = os.path.join(node.getModule().getLocalPath(),\
								  node.getOutputFile())
	outdir,leaf = os.path.split(outfile)
	if not os.path.exists(outdir):
		os.makedirs(outdir)
		
	srcfile = node.getSourcePath()
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
		print "Writing %s..." % outfile
		html = node.render_html(request=None)
		open(outfile,"w").write(html)

	for (name,childNode) in node.getChildren().items():
		_wmm2html(childNode,force) #os.path.join(outdir,name),force)


def wmm2html(srcdir,outdir=None,force=False,showOutput=True):
	"""convert a complete module to static html
	"""
	#
	if outdir is None:
		outdir = srcdir

	site = Site(srcdir)

	site.init()
	
	_wmm2html(site.root,force)

	if showOutput:
		import webbrowser
		webbrowser.open(os.path.join(outdir,'index.html'),new=True)

