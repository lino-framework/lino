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

from lino.apps.keeper.tables import *
from lino.apps.keeper.tables import TABLES
from lino.adamo.ddl import Schema, Populator, STRING
from lino.reports import DataReport
from lino.misc.tsttools import TESTDATA

class TestPopulator(Populator):
    def populateVolumes(self,q):
        q.appendRow(path=TESTDATA)
        
class Keeper(Schema):
    
    years='2005'
    author="Luc Saffre"
    
    tables = TABLES

    def showSearchForm(self,sess):
        searchData = sess.query(Files,"name")
        occs=searchData.addColumn("occurences")
        
        frm = sess.form(label="Search")

        searchString = frm.addEntry("searchString",STRING,
                                    label="Words to look for",
                                    value="")
        def search():
            #self.searchData.setSarch(searchString.getValue())
            occs._queryParams["search"]=searchString.getValue()
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
        rpt=DataReport(searchData)
        bbox.addDataGrid(rpt)

        frm.show()
        #frm.showModal()



    def showMainForm(self,sess):
        frm = sess.form(
            label="Main menu",
            doc="""\
This is the Keeper main menu.                                    
"""+("\n"*10))

        m = frm.addMenu("search","&Suchen")
        m.addItem("search",label="&Suchen").setHandler(
            self.showSearchForm,sess)
    
        m = frm.addMenu("db","&Datenbank")
        m.addItem("volumes",label="&Volumes").setHandler(
            sess.showViewGrid, Volumes)
        m.addItem("files",label="&Files").setHandler(
            sess.showViewGrid, Files)
        m.addItem("dirs",label="&Directories").setHandler(
            sess.showViewGrid, Directories)
        m.addItem("words",label="&Words").setHandler(
            sess.showViewGrid, Words)
        
        self.addProgramMenu(sess,frm)

        frm.addOnClose(sess.close)

        frm.show()


if __name__ == '__main__':
    from lino.forms import gui
    app=Keeper()
    sess=app.quickStartup()
    sess.populate(TestPopulator())
    gui.run(sess)
