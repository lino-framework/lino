## Copyright 2002-2007 Luc Saffre 

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

"""
create thumbnails and web-sized images if necessary
  
New naming scheme : the separate "thumbnails" tree used by publish is
replaced with the more "normal" method using "_tn" suffix.
  
"""

import os

from PIL import Image

from lino.console.application import Application

class Size:
	def __init__(self,suffix,size):
		self.suffix = "_" + suffix
		self.size = size


def webify(filename):
    return filename.replace(" ","_")

class MakeThumbnails(Application):

    name="Lino/maketn"

    copyright="""\
Copyright (c) 2002-2007 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    usage="usage: %prog [options] DIR1 [DIR2 ...]"
    
    description="""\
where DIR1 DIR2... are the root directories to be processed.
Subdirectories of these directories will automatically be
processed.

"""

    sizes = [ #Size("tn",(128,128)),
        Size("web",(512,512)) ]

    #EXTENSIONS = (".jpg",".png")
    extensions = (".jpg")



    def make_tn(self,path):
        for fn in os.listdir(path):
            pfn = os.path.join(path,fn)
            if os.path.isdir(pfn):
                self.make_tn(pfn)
            else:
                (root,ext) = os.path.splitext(pfn)
                #(root,ext) = os.path.splitext(fn)
                if not ext in self.extensions:
                    continue
                if " " in root:
                    self.warning("Skipping %s : spaces are not allowed!",pfn)
                    continue
                is_original=True
                for size in self.sizes:
                    if root.endswith(size.suffix):
                        is_original=False
                        ofn=os.path.join(path,root[0:-len(size.suffix)])+ext
                        if not os.path.exists(ofn):
                            self.warning("%s has no original (%s)!",pfn,ofn)
                if is_original:
                    self.count_originals += 1
                    for size in self.sizes:
                        #1 tfn = os.path.join(path,root) + size.suffix + ext
                        tfn = root + size.suffix + ext
                        # TODO : check whether it is older than original
                        if not os.path.exists(tfn):
                            self.verbose("%s -> %s" % (pfn,tfn))
                            im = Image.open(pfn)
                            im.thumbnail(size.size) 
                            im.save(tfn)
                            self.count_created += 1



    def run(self):

        self.count_created=0
        self.count_originals=0

        if len(self.args) == 0:
            dirs=['.']
        else:
            dirs=self.args

        for dirname in dirs:
            self.make_tn(dirname)
            
        if self.count_created == 0:
            self.notice("Nothing to do.")
        else:
            self.notice("Created %d thumbnails from %d originals.",
                        self.count_created,self.count_originals)

def main(*args,**kw):
    MakeThumbnails().main(*args,**kw)
    
