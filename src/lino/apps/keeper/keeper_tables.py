#coding: latin1

## Copyright 2004-2005 Luc Saffre

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

from lino.adamo import *
from lino.schemas.sprl.babel import Languages

class Volumes(Table):
    def init(self):
        self.addField('id',ROWID) 
        self.addField('name',STRING)
        self.addField('meta',MEMO(width=50,height=5))
        self.addField('path',STRING)

    def setupMenu(self,nav):
        frm = nav.getForm()
        m = frm.addMenu("&Volume")
        def f():
            vol = nav.getCurrentRow()
            vol.load(frm)
            
        m.addItem(label="&Load",
                  action=f,
                  accel="F6")

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name
        def load(self,ui):
            from lino.apps.keeper.populate import VolumeVisitor
            VolumeVisitor(self).run(ui)
    
        
class Directories(Table):
    def init(self):
        self.addField('id',ROWID) 
        self.addField('name',STRING)
        #self.addField('mtime',TIMESTAMP)
        self.addField('meta',MEMO(width=50,height=5))
        self.addPointer('parent',Directories)
        self.addPointer('volume',Volumes)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name
        def path(self):
            if self.parent is None:
                return self.name
            return os.path.join(self.parent.path(),self.name)

class Files(Table):
    def init(self):
        self.addField('id',ROWID) 
        self.addField('name',STRING)
        #self.addField('mtime',TIMESTAMP)
        self.addField('meta',MEMO(width=50,height=5))
        self.addPointer('dir',Directories)
        self.addPointer('type',FileTypes)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name
        def path(self):
            return os.path.join(self.dir.path(),self.name)

class FileTypes(Table):
    def init(self):
        self.addField('id',STRING(width=5))
        self.addField('name',STRING)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name
        
class Words(Table):
    def init(self):
        self.addField('id',ROWID)
        self.addField('word',STRING)
        self.addPointer('synonym',Words)

    class Instance(Table.Instance):
        def getLabel(self):
            return self.name

class Occurences(Table):
    def init(self):
        self.addPointer('word',Words)
        self.addPointer('file',Files)
        self.addField('pos',INT)

    class Instance(Table.Instance):
        pass
# order of tables is important: tables will be populated in this order
TABLES = (
    Volumes,
    Files,
    Directories,
    FileTypes,
    Words,
    Occurences,
    )


def setupSchema(schema):
    for t in TABLES:
        schema.addTable(t)

