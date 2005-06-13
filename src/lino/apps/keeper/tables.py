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

import os

from lino.adamo.ddl import *
from lino.apps.keeper.populate import VolumeVisitor

class Volumes(Table):
    
    def init(self):
        self.addField('id',ROWID) 
        self.addField('name',STRING)
        self.addField('meta',MEMO(width=50,height=5))
        self.addField('path',STRING)
        #self.addDetail('directories',Directories,parent=None)
        self.addView("std", "id name path directories meta")
        

    def setupMenu(self,nav):
        frm = nav.getForm()
        m = frm.addMenu("&Volume")
        def f():
            vol = nav.getCurrentRow()
            vol.load(frm)
            
        m.addItem("load",
                  label="&Load",
                  action=f,
                  accel="F6")

    class Instance(Table.Instance):
        def __str__(self):
            if self.name is not None: return self.name
            return self.path
        
        def load(self,ui):
            VolumeVisitor(self).run(ui)

        def delete(self):
            self.directories.deleteAll()
            
        
class Directories(Table):
    def init(self):
        self.addField('id',ROWID) 
        self.addField('name',STRING)
        #self.addField('mtime',TIMESTAMP)
        self.addField('meta',MEMO(width=50,height=5))
        self.addPointer('parent',Directories).setDetail(
            "subdirs",viewName="std")
        self.addPointer('volume',Volumes).setDetail(
            "directories",parent=None,viewName="std")
        self.addView("std","parent name subdirs files meta volume")
        #self.setPrimaryKey("volume parent name")

    class Instance(Table.Instance):
        def __str__(self):
            return self.name
        def path(self):
            if self.parent is None:
                return self.name
            return os.path.join(self.parent.path(),self.name)
        
        def delete(self):
            #print "Delete entry for ",self
            assert not self in self.subdirs
            self.files.deleteAll()
            self.subdirs.deleteAll()
##             for row in self.files:
##                 row.delete()
##             for row in self.subdirs:
##                 row.delete()
            Table.Instance.delete(self)
                

class Files(Table):
    def init(self):
        #self.addField('id',ROWID) 
        self.addField('name',STRING).setMandatory()
        #self.addField('mtime',TIMESTAMP)
        self.addField('meta',MEMO(width=50,height=5))
        self.addPointer('dir',Directories).setDetail(
            "files",orderBy="name")
        self.addPointer('type',FileTypes)
        self.setPrimaryKey("dir name")
        self.addView("std","dir name type meta")

    class Instance(Table.Instance):
        
        def __str__(self):
            return self.name
        
        def path(self):
            return os.path.join(self.dir.path(),self.name)
        
class FileTypes(Table):
    def init(self):
        self.addField('id',STRING(width=5))
        self.addField('name',STRING)

    class Instance(Table.Instance):
        def __str__(self):
            return self.name
        
class Words(Table):
    def init(self):
        self.addField('id',STRING)
        #self.addField('word',STRING)
        self.addPointer('synonym',Words)
        #self.addField('ignore',BOOL)
        self.addView("std","id synonym occurences")

    class Instance(Table.Instance):
        pass
        #def __str__(self):
        #    return self.id

class Occurences(Table):
    def init(self):
        self.addPointer('word',Words).setDetail("occurences")
        self.addPointer('file',Files).setDetail("occurences")
        self.addField('pos',INT)
        self.setPrimaryKey("word file pos")

    class Instance(Table.Instance):
        pass



TABLES = (
    Volumes,
    Files,
    Directories,
    FileTypes,
    Words,
    Occurences,
    )

__all__ = [t.__name__ for t in TABLES]

