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

from lino.forms import gui

from lino.apps.keeper import tables
from lino.adamo.ddl import Schema

class Keeper(Schema):
    
    years='2005'
    author="Luc Saffre"
    
    tables = tables.TABLES

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

        m = frm.addMenu("search","&Suchen")
        m.addItem("search",label="&Suchen").setHandler(
            self.showSearchForm,frm)
    
        m = frm.addMenu("db","&Datenbank")
        m.addItem("volumes",label="&Volumes").setHandler(
            self.showViewGrid,frm,
            Volumes)
        m.addItem("files",label="&Files").setHandler(
            self.showViewGrid,frm,
            Files)
        m.addItem("dirs",label="&Directories").setHandler(
            self.showViewGrid,frm,
            Directories)
        m.addItem("words",label="&Words").setHandler(
            self.showViewGrid,frm,
            Words)
        
        self.addProgramMenu(frm)

        frm.addOnClose(self.close)

        frm.show()


if __name__ == '__main__':
    app=Keeper()
    app.parse_args()
    gui.run(app)
