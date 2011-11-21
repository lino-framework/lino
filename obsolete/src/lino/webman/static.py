#coding: latin1

## Copyright Luc Saffre 2003-2004.

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os,sys
from time import asctime, localtime

from docutils import core
from nodes import WebModule, TxtWebPage
from sitemap import Site

from lino.ui import console 

## DEFAULTS = {'input_encoding': 'latin-1',
##              'output_encoding': 'latin-1',
##              'stylesheet_path': 'default.css',
##              'source_link': 1,
##              'tab_width': 3,
##              'datestamp' : '%Y-%m-%d %H:%M UTC',
##              'generator': 1 
##              }


def node2html(node,destRoot,force=False):
    
    """ TODO: Analysefehler: wenn mehrere Dateien erzeugt werden, muss
    hier noch was geändert werden...
    
    """
    outdir = os.path.join(destRoot,*node.getLocation())
    outfile = os.path.join(outdir,node.getOutputFile())
    #node.getOutputFile():
    #outfile = os.path.join(node.getModule().getLocalPath(),\
    #                             node.getOutputFile())
    #outdir,leaf = os.path.split(outfile)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    updodate = False
    assert node.modified is not None, str(node)
    if not force:
        try:
            if os.path.getmtime(outfile) > node.modified:
                updodate = True
        except os.error:
            pass
    if updodate:
        console.info("%s : up to date" % outfile)
    else:
        console.progress("Writing %s ..." % outfile)
        #print asctime(localtime(node.modified)))
        html = node.render_html(request=None)
        open(outfile,"w").write(html)

    for child in node.getChildren():
        node2html(child,destRoot,force) 


def wmm2html(srcdir,
             files=None,
             outdir=None,
             force=False):
    """convert a complete module to static html
    """
    #
    if outdir is None:
        outdir = srcdir

    site = Site(srcdir)

    site.init()
    
    node2html(site.root,outdir,force)

    if console.confirm("Show output?",default="n"):
        import webbrowser
        webbrowser.open(os.path.join(outdir,'index.html'),new=True)

