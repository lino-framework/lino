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

from lino.adamo.tabledef import *
from lino.forms import gui

#from lino.apps.keeper import keeper_tables as tables

from lino.adamo.schema import Schema

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
            
        m.addItem(label="&Load",
                  action=f,
                  accel="F6")

    class Instance(Table.Instance):
        def getLabel(self):
            if self.name is not None: return self.name
            return self.path
        
        def load(self,ui):
            from lino.apps.keeper.populate import VolumeVisitor
            VolumeVisitor(self).run(ui)
    
        
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
        def getLabel(self):
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
        self.addField('name',STRING)
        #self.addField('mtime',TIMESTAMP)
        self.addField('meta',MEMO(width=50,height=5))
        self.addPointer('dir',Directories).setDetail(
            "files",orderBy="name")
        self.addPointer('type',FileTypes)
        self.setPrimaryKey("dir name")
        self.addView("std","dir name type meta")

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
        self.addField('id',STRING)
        #self.addField('word',STRING)
        self.addPointer('synonym',Words)
        #self.addField('ignore',BOOL)
        self.addView("std","id synonym occurences")

    class Instance(Table.Instance):
        pass
        #def getLabel(self):
        #    return self.id

class Occurences(Table):
    def init(self):
        self.addPointer('word',Words).setDetail("occurences")
        self.addPointer('file',Files).setDetail("occurences")
        self.addField('pos',INT)
        self.setPrimaryKey("word file pos")

    class Instance(Table.Instance):
        pass




class Keeper(Schema):
    
    name="Keeper"
    years='2005'
    author="Luc Saffre"
    
    tables = (
        Volumes,
        Files,
        Directories,
        FileTypes,
        Words,
        Occurences,
        )

    def showSearchForm(self,ui):
        self.searchData = self.sess.query(Files,"name")
        self.occs=self.searchData.addColumn("occurences")
        
        frm = ui.form(label="Search")

        searchString = frm.addEntry("searchString",adamo.STRING,
                                    label="Words to look for",
                                    value="")
        def search():
            #self.searchData.setSarch(searchString.getValue())
            self.occs._queryParams["search"]=searchString.getValue()
            frm.refresh()
            #a = self.arrivals.appendRow(
            #    dossard=frm.entries.dossard.getValue(),
            #    time=now.time())
            #frm.status("%s arrived at %s" % (a.dossard,a.time))
            #searchString.setValue('')
            #frm.entries.dossard.setFocus()



        #bbox = frm.addHPanel()
        bbox = frm
        bbox.addButton("search",
                       label="&Search",
                       action=search).setDefault()
        #bbox.addButton("exit",
        #               label="&Exit",
        #               action=frm.close)

        bbox.addDataGrid(self.searchData)

        frm.show()
        #frm.showModal()



    def showMainForm(self,ui):
        frm = ui.form(
            label="Main menu",
            doc="""\
This is the Keeper main menu.                                     
"""+("\n"*10))

        m = frm.addMenu("&Suchen")
        m.addItem(label="&Suchen").setHandler(
            self.showSearchForm,frm)
    
        m = frm.addMenu("&Datenbank")
        m.addItem(label="&Volumes").setHandler(
            self.showViewGrid,frm,
            Volumes)
        m.addItem(label="&Files").setHandler(
            self.showViewGrid,frm,
            Files)
        m.addItem(label="&Directories").setHandler(
            self.showViewGrid,frm,
            Directories)
        m.addItem(label="&Words").setHandler(
            self.showViewGrid,frm,
            Words)
        
        self.addProgramMenu(frm)

        frm.addOnClose(self.close)

        frm.show()

## def main(argv):

##     app=Keeper()
##     app.parse_args()
##     app.run()
    

## if __name__ == '__main__':
##     main(sys.argv[1:])


if __name__ == '__main__':
    app=Keeper()
    app.parse_args()
    app.run()
