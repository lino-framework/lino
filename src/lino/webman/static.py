#coding: latin1
#----------------------------------------------------------------------
# static.py
# Copyright: (c) 2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------
import os,sys
from time import asctime, localtime

from docutils import core
from nodes import WebModule, TxtWebPage
from sitemap import Site

## DEFAULTS = {'input_encoding': 'latin-1',
## 				'output_encoding': 'latin-1',
## 				'stylesheet_path': 'default.css',
## 				'source_link': 1,
## 				'tab_width': 3,
## 				'datestamp' : '%Y-%m-%d %H:%M UTC',
## 				'generator': 1 
## 				}


def node2html(node,destRoot,force=False):
	
	""" TODO: Analysefehler: wenn mehrere Dateien erzeugt werden, muss
	hier noch was geändert werden...
	
	"""
	outdir = os.path.join(destRoot,*node.getLocation())
	outfile = os.path.join(outdir,node.getOutputFile())
	#node.getOutputFile():
	#outfile = os.path.join(node.getModule().getLocalPath(),\
	#							  node.getOutputFile())
	#outdir,leaf = os.path.split(outfile)
	if not os.path.exists(outdir):
		os.makedirs(outdir)

	updodate = False
	assert node.modified is not None, str(node)
	if not force:
		try:
			if os.path.getmtime(outfile) < node.modified:
				updodate = True
		except os.error:
			pass
	if updodate:
		print "%s : up to date" % outfile
	else:
		print "Writing %s ..." % outfile
		#print asctime(localtime(node.modified)))
		html = node.render_html(request=None)
		open(outfile,"w").write(html)

	for child in node.getChildren():
		node2html(child,destRoot,force) 


def wmm2html(srcdir,outdir=None,force=False,showOutput=True):
	"""convert a complete module to static html
	"""
	#
	if outdir is None:
		outdir = srcdir

	site = Site(srcdir)

	site.init()
	
	node2html(site.root,outdir,force)

	if showOutput:
		import webbrowser
		webbrowser.open(os.path.join(outdir,'index.html'),new=True)

