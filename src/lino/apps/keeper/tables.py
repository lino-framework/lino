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
from lino.apps.keeper.populate import VolumeVisitor, read_content

from lupy.index.documentwriter import standardTokenizer

class Volumes(Table):
    
    def init(self):
        self.addField('id',ROWID) 
        self.addField('name',STRING).setMandatory()
        self.addField('meta',MEMO(width=50,height=5))
        self.addField('path',STRING).setMandatory()
        #self.addDetail('directories',Directories,parent=None)
        self.addView("std", "id name path directories meta")
        

    def setupMenu(self,nav):
        frm = nav.getForm()
        m = frm.addMenu("&Volume")
        def f():
            vol = nav.getCurrentRow()
            vol.item.load(frm.session)
            
        m.addItem("load",
                  label="&Load",
                  action=f,
                  accel="F6")

    class Instance(Table.Instance):
        def __str__(self):
            return self.name
            #if self.name is not None: return self.name
            #return self.path
        
        def load(self,sess):
            sess.runTask(VolumeVisitor(self))

        def delete(self):
            self.directories.deleteAll()

        def ignoreByName(self,name):
            if name is None: return False
            if name.endswith('~'): return True
            return name in ('.svn',)
            
        
class Directories(Table):
    def init(self):
        self.addField('id',ROWID) 
        self.addField('name',STRING) # .setMandatory()
        #self.addField('mtime',TIMESTAMP)
        self.addField('meta',MEMO(width=50,height=5))
        self.addPointer('parent',Directories).setDetail(
            "subdirs")#,viewName="std")
        self.addPointer('volume',Volumes).setDetail(
            "directories",parent=None)#,viewName="std")
        self.addView("std","parent name subdirs files meta volume")
        #self.setPrimaryKey("volume parent name")

    class Instance(Table.Instance):
        
        def __str__(self):
            s=str(self.volume) +":"
            if self.name is not None:
                s += self.name
            return s
        
        def path(self):
            if self.parent is None:
                if self.name is None:
                    return self.volume.path
                return os.path.join(self.volume.path,self.name)
            else:
                if self.name is None:
                    return self.parent.path()
                else:
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
        self.addField('mtime',TIMESTAMP)
        self.addField('size',LONG)
        self.addField('content',MEMO(width=50,height=5))
        self.addField('meta',MEMO(width=50,height=5))
        self.addPointer('dir',Directories).setDetail(
            "files",orderBy="name")
        self.addPointer('type',FileTypes)
        self.addField('mustParse',BOOL)
        
        self.setPrimaryKey("dir name")
        self.addView(
            "std",
            """\
dir name type
mtime size mustParse
content
meta
""")

        
    class Instance(Table.Instance):
        
        def __str__(self):
            assert self.name is not None
            return self.name
        
        def path(self):
            return os.path.join(self.dir.path(),self.name)
        
        def readTimeStamp(self,sess,fullname):
            #assert fullname == self.path(), \
            #       "%r != %r" % (fullname,self.path())
            try:
                st = os.stat(fullname)
            except OSError,e:
                sess.error("os.stat('%s') failed" % fullname)
                return
            sz = st.st_size
            mt = st.st_mtime
            if self.mtime == mt and self.size == sz:
                return
            self.lock()
            self.content=read_content(sess,self,fullname)
            self.mtime = mt
            self.size=sz
            self.mustParse=True
            self.parseContent(sess)
            self.unlock()

        def parseContent(self,sess):
            if self.content is None:
                return
            tokens = standardTokenizer(self.content)
            self.occurences.deleteAll()
            words=sess.query(Words)
            pos = 0
            for token in tokens:
                pos += 1
                sess.status(self.path()+": "+token)
                word = words.peek(token)
                if word is None:
                    word = words.appendRow(id=token)
                #elif word.ignore:
                #    continue
                self.occurences.appendRow(word=word, pos=pos)
        
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

