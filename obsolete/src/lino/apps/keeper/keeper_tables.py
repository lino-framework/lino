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
from types import StringType

from lino.adamo.ddl import *
from lino.adamo.filters import Contains, NotEmpty
#from lino.forms.session import Session
from lino.apps.keeper.populate import \
     VolumeVisitor, read_content,\
     standardTokenizer

#from lupy.index.documentwriter import standardTokenizer

def preview(s):
    if len(s) < 100: return s
    return s[:100]+" (...)"


class Volume(StoredDataRow):
    tableName="Volumes"
    def initTable(self,table):
        table.addField('id',ROWID) 
        table.addField('name',STRING).setMandatory()
        table.addField('meta',MEMO(width=50,height=5))
        table.addField('path',STRING).setMandatory()
        #table.addDetail('directories',Directories,parent=None)
        #table.addView("std", "id name path directories meta")
        table.addDetail('directories',Directory,'volume',parent=None)
        

    def setupMenu(self,frm):
        #frm = nav.getForm()
        m = frm.addMenu("volume",label="&Volume")
        def f():
            vol = frm.getCurrentRow()
            vol.item.load()
            
        m.addItem("load",
                  label="&Load",
                  action=f,
                  accel="F6")

    def getLabel(self):
        return self.name
        
    def load(self,toolkit):
        toolkit.runtask(VolumeVisitor(self))
        #sess.loop(vv.looper,"Loading %s" % self.name)

    def delete(self):
        self.directories().deleteAll()

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
        table.addPointer('parent',Directory)
        table.addPointer('volume',Volume)
        table.addDetail('files',File,'dir')
        table.addDetail('subdirs',Directory,'parent')
        #self.setPrimaryKey("volume parent name")

    def getLabel(self):
        s=self.volume.getLabel() +":"
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
        self.files().deleteAll()
        self.subdirs().deleteAll()
        StoredDataRow.delete(self)
                
class DirectoriesReport(DataReport):
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
        table.addPointer('dir',Directory)
        #.setDetail("files",orderBy="name")
        table.addPointer('type',FileType)
        table.addField('mustParse',BOOL)
        
        table.setPrimaryKey("dir name")
        table.addDetail('occurences',Occurence,'file')
##         table.addView(
##             "std",
##             """\
## dir name type
## mtime size mustParse
## content
## meta
## """)

        
    def getLabel(self):
        assert self.name is not None
        return self.name

    def path(self):
        return os.path.join(self.dir.path(),self.name)

    def readTimeStamp(self,ui,fullname):
        try:
            st = os.stat(fullname)
        except OSError,e:
            ui.error("os.stat('%s') failed" % fullname)
            return
        sz = st.st_size
        mt = st.st_mtime
        if self.mtime == mt and self.size == sz:
            return
        self.lock()
        s=read_content(ui,self,fullname)
        if s and len(s.strip()) > 0:
            #"assert UnicodeString if not pure ascii"
            #assert ispure(s)
            #if type(s) == StringType:
            #    s=s.decode('ascii')
            self.content=s
        self.mtime = mt
        self.size=sz
        self.mustParse=True
        self.parseContent(ui)
        self.unlock()

    def parseContent(self,ui):
        if self.content is None:
            return
        tokens = standardTokenizer(self.content)
        occs=self.occurences()
        occs.deleteAll()
        words=self.getContext().query(Word)
        pos = 0
        for token in tokens:
            pos += 1
            ui.status(self.path()+": "+token)
            word = words.peek(token)
            if word is None:
                word = words.appendRow(id=token)
            #elif word.ignore:
            #    continue
            occs.appendRow(word=word, pos=pos)
        
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

    def getLabel(self):
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
        table.addDetail('occurences',Occurence,'word')

class WordsReport(DataReport):
    leadTable=Word
    columnNames="id synonym occurences"
    
class Occurence(StoredDataRow):
    tableName="Occurences"
    def initTable(self,table):
        table.addPointer('word',Word)
        #.setDetail("occurences")
        table.addPointer('file',File)
        #.setDetail("occurences")
        table.addField('pos',INT)
        table.setPrimaryKey("word file pos")

class OccurencesReport(DataReport):
    leadTable=Occurence


class FoundFilesReport(DataReport):
    leadTable=File
    #width=70
    
    def setupReport(self):
        assert len(self.columns) == 0
        #files = self.query.session.query(tables.File) #,"name")
        self.addDataColumn("name",width=20)
        occsColumn=self.addDataColumn(
            "occurences",
            formatter=lambda pq: str(len(pq())),\
            #searchColumns="words.id",
            label="occs",
            width=5)
        self.addDataColumn("content",
                           width=40,
                           formatter=lambda x: preview(x))

        self.occsColumn=occsColumn.datacol
        self.query.addFilter(NotEmpty(self.occsColumn))
        #self.occs=col.getDetailQuery()
        self.occsColumn._queryParams['searchColumns']="word.id"
        
    def setSearch(self,s):
        self.occsColumn._queryParams['search'] = s


    
    
class KeeperSchema(Schema):
    tableClasses = ( 
        Volume,
        File,
        Directory,
        FileType,
        Word,
        Occurence
        )


class SearchForm(ReportForm):
    
    title="Search"
    
    def layout(self,panel):
        
        #dbsess=self.rpt.query.getContext()
        #words = sess.query(tables.Word)
        #files = sess.query(tables.File) #,"name")
        #grid=None # referenced in search(), defined later
        

        self.searchString=panel.entry(
            STRING,
            label="&Words to look for")
        self.anyWord=panel.entry(BOOL,label="&any word (OR)")
        
        def search():
##             files.clearFilters()
##             for word in searchString.getValue().split():
##                 w=words.peek(word)
##                 if w is None:
##                     sess.notice("ignored '%s'"%w)
##                 else:
##                     occs.addFilter(Contains,w)
                
            #files.setSearch(searchString.getValue())
            #occs._queryParams["search"]=searchString.getValue()
            self.rpt.setSearch(self.searchString.getValue())
            self.grid.enabled=self.searchString.getValue() is not None
            self.refresh()



        #bbox = panel.hpanel()
        bbox = panel
        self.go = bbox.button("search",
                              label="&Search",
                              action=search).setDefault()
        #bbox.addButton("exit",
        #               label="&Exit",
        #               action=frm.close)
        self.grid=panel.datagrid(self.rpt)
        #ReportForm.setupForm(self)
        self.grid.enabled=False



class KeeperMainForm(DbMainForm):

    schemaClass=KeeperSchema
    
    def layout(self,panel):
        panel.label("""

Keeper keeps an eye on your files. He knows your files and helps you
to find them back even if they are archived on external media.
(But please note that Keeper is not yet in a usable state.)

        """)
    
    def setupMenu(self):

        m = self.addMenu("search","&Search")
        m.addItem("search",label="&Search").setHandler(
            self.showForm,
            SearchForm(FoundFilesReport(self.dbsess)))

        
    
        m = self.addMenu("db","&Database")

        self.addReportItem(
            m,"volumes",VolumesReport,
            label="&Volumes")
        self.addReportItem(
            m,"files",FilesReport,
            label="&Files")
        self.addReportItem(
            m,"dirs",DirectoriesReport,
            label="&Directories")
        self.addReportItem(
            m, "words",WordsReport,
            label="&Words")
        
        self.addProgramMenu()


class Keeper(DbApplication):
    
    name="Lino Keeper"
    version="0.0.1"
    copyright="""\
Copyright (c) 2004-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    mainFormClass=KeeperMainForm

        


    

__all__ = [t.__name__ for t in KeeperSchema.tableClasses]
__all__.append('Keeper')
__all__.append('KeeperSchema')
__all__.append('FoundFilesReport')
__all__.append('SearchForm')

