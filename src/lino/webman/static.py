import os,sys

from docutils import core
from nodes import Site, WebModule, TxtWebPage

## DEFAULTS = {'input_encoding': 'latin-1',
## 				'output_encoding': 'latin-1',
## 				'stylesheet_path': 'default.css',
## 				'source_link': 1,
## 				'tab_width': 3,
## 				'datestamp' : '%Y-%m-%d %H:%M UTC',
## 				'generator': 1 
## 				}


def node2html(node,force=False):
	for outfile in node.getOutputFiles():
		#outfile = os.path.join(node.getModule().getLocalPath(),\
		#							  node.getOutputFile())
		outdir,leaf = os.path.split(outfile)
		if not os.path.exists(outdir):
			os.makedirs(outdir)

		updodate = False
		if not force:
			try:
				if os.path.getmtime(outfile) > node.modified:
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
		node2html(childNode,force) 


def wmm2html(srcdir,outdir=None,force=False,showOutput=True):
	"""convert a complete module to static html
	"""
	#
	if outdir is None:
		outdir = srcdir

	site = Site(srcdir)

	site.init()
	
	node2html(site.root,force)

	if showOutput:
		import webbrowser
		webbrowser.open(os.path.join(outdir,'index.html'),new=True)

