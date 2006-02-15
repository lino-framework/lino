#coding: latin1
## Copyright 2005-2006 Luc Saffre 

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
from lino.forms.session import Session
from lino.apps.keeper.populate import VolumeVisitor, read_content

from lupy.index.documentwriter import standardTokenizer


class Volume(StoredDataRow):
    tableName="Volumes"
    def initTable(self,table):
        table.addField('id',ROWID) 
        table.addField('name',STRING).setMandatory()
        table.addField('meta',MEMO(width=50,height=5))
        table.addField('path',STRING).setMandatory()
        #table.addDetail('directories',Directories,parent=None)
        #table.addView("std", "id name path directories meta")
        

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

    def __str__(self):
        return self.name
        
    def load(self,sess):
        vv=VolumeVisitor(self)
        sess.loop(vv.looper,"Loading %s" % self.name)

    def delete(self):
        self.directories.deleteAll()

    def ignoreByName(self,name):
        if name is None: return False
        if name.endswith('~'): return True
        return name in ('.svn',)

class VolumesReport(DataReport):
    leadTable=Volume
    columnNames="id name path directories meta"
            
        
class Directory(StoredDataRow):
    tableName="Directories"
    def initTable(self,table):
        table.addField('id',ROWID) 
        table.addField('name',STRING) # .setMandatory()
        #table.addField('mtime',TIMESTAMP)
        table.addField('meta',MEMO(width=50,height=5))
        table.addPointer('parent',Directory).setDetail(
            "subdirs")#,viewName="std")
        table.addPointer('volume',Volume).setDetail(
            "directories",parent=None)#,viewName="std")
        #table.addView("std","parent name subdirs files meta volume")
        #self.setPrimaryKey("volume parent name")

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
        StoredDataRow.delete(self)
                
class DiretoriesReport(DataReport):
    leadTable=Directory
    columnNames="parent name subdirs files meta volume"
            

class File(StoredDataRow):
    tableName="Files"
    def initTable(self,table):
        #table.addField('id',ROWID) 
        table.addField('name',STRING).setMandatory()
        table.addField('mtime',TIMESTAMP)
        table.addField('size',LONG)
        table.addField('content',MEMO(width=50,height=5))
        table.addField('meta',MEMO(width=50,height=5))
        table.addPointer('dir',Directory).setDetail(
            "files",orderBy="name")
        table.addPointer('type',FileType)
        table.addField('mustParse',BOOL)
        
        table.setPrimaryKey("dir name")
##         table.addView(
##             "std",
##             """\
## dir name type
## mtime size mustParse
## content
## meta
## """)

        
    def __str__(self):
        assert self.name is not None
        return self.name

    def path(self):
        return os.path.join(self.dir.path(),self.name)

    def readTimeStamp(self,sess,fullname):
        assert isinstance(sess,Session), \
               "%s is not a Session" % sess.__class__
        #assert sess.__class__.__name__ == 'Session', \
        #       "%s is not a Session" % sess.__class__
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
        s=read_content(sess,self,fullname)
        if s and len(s.strip()) > 0: 
            self.content=s
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
        words=sess.query(Word)
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
        
class FilesReport(DataReport):
    leadTable=File
    columnNames="""\
dir name type
mtime size mustParse
content
meta
"""
            
class FileType(StoredDataRow):
    tableName="FileTypes"
    def initTable(self,table):
        table.addField('id',STRING(width=5))
        table.addField('name',STRING)

    def __str__(self):
        return self.name
        
class FileTypesReport(DataReport):
    leadTable=FileType
    
class Word(StoredDataRow):
    tableName="Words"
    def initTable(self,table):
        table.addField('id',STRING)
        #table.addField('word',STRING)
        table.addPointer('synonym',Word)
        #table.addField('ignore',BOOL)
        #table.addView("std","id synonym occurences")

class WordsReport(DataReport):
    leadTable=Word
    columnNames="id synonym occurences"
    
class Occurence(StoredDataRow):
    tableName="Occurences"
    def initTable(self,table):
        table.addPointer('word',Word).setDetail("occurences")
        table.addPointer('file',File).setDetail("occurences")
        table.addField('pos',INT)
        table.setPrimaryKey("word file pos")

class OccurencesReport(DataReport):
    leadTable=Occurence
    

TABLES = (
    Volume,
    File,
    Directory,
    FileType,
    Word,
    Occurence,
    )

__all__ = [t.__name__ for t in TABLES]

