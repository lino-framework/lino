#coding: latin1
## Copyright 2005 Luc Saffre 

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

import sys
import os
opj = os.path.join

from lino.apps.keeper import keeper_tables as tables
from lino.ui import console
from lino.misc.jobs import Task

class VolumeVisitor(Task):
    def __init__(self,vol):
        Task.__init__(self)
        self.volume = vol

    def start(self):
        sess = self.volume.getSession()
        self.ftypes = sess.query(tables.FileTypes)
        self.files = sess.query(tables.Files)
        self.dirs = sess.query(tables.Directories)
        self.words = sess.query(tables.Words)
        self.occs = sess.query(tables.Occurences)
        for row in self.dirs.query(volume=self.volume):
            row.delete()
        self.schedule(self.visit,self.volume.path,"")

    def getLabel(self):
        return "Loading "+self.volume.getLabel()

    def visit(self,fullname,shortname,dir=None):
        if os.path.isfile(fullname):
            row = self.files.peek(dir,shortname)
            if row is None:
                row = self.files.appendRow(name=shortname,dir=dir)
            self.visit_file(row,fullname)
        elif os.path.isdir(fullname):
            #print "findone(",dict(parent=dir,name=shortname),")"
            row = self.dirs.findone(parent=dir,name=shortname)
            if row is None:
                row = self.dirs.appendRow(name=shortname,
                                          parent=dir,
                                          volume=self.volume)
            self.visit_dir(row,fullname)
        else:
            raise SyncError(
                "%s is neither file nor directory" % src)

    def visit_file(self,row,name):
        base,ext = os.path.splitext(name)
        if ext == ".txt":
            count = 0
            for ln in open(name).readlines():
                for w in ln.split():
                    count += 1
            self.info("%s contains %d words." % (name,count))
                    
    
    def visit_dir(self,row,fullname):
        self.warning("visit_dir " + fullname)
        for fn in os.listdir(fullname):
            self.schedule(self.visit,
                          os.path.join(fullname,fn),
                          fn,
                          row)
        
    def readTimeStamp(self,row,filename):
        try:
            st = os.stat(filename)
            sz = st.st_size
            mt = st.st_mtime
        except OSError,e:
            self.error("os.stat('%s') failed" % filename)
            return
        row.mtime = x

        
