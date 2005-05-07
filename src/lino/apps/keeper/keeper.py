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

from lino import adamo
from lino.forms import gui

from lino.apps.keeper import keeper_tables as tables

from lino.adamo.application import AdamoApplication


class Keeper(AdamoApplication):
    
    name="Keeper"
    years='2005'
    author="Luc Saffre"
    
    def showSearchForm(self,ui):
        self.searchData = self.sess.query(tables.Files,"name")
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


    def init(self):
        tables.setupSchema(self.schema)
        
        self.sess = self.schema.quickStartup(
            ui=self.toolkit.console,
            filename=self.filename)
        
        #assert self.mainForm is None
        
        #self.mainForm = frm = self.form(
        frm = self.form(
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
            tables.Volumes)
        m.addItem(label="&Files").setHandler(
            self.showViewGrid,frm,
            tables.Files)
        m.addItem(label="&Directories").setHandler(
            self.showViewGrid,frm,
            tables.Directories)
        m.addItem(label="&Words").setHandler(
            self.showViewGrid,frm,
            tables.Words)
        
        self.addProgramMenu(frm)

        frm.addOnClose(self.close)

        frm.show()

def main(argv):

    app = Keeper()
    app.parse_args()
    app.run()
    

if __name__ == '__main__':
    main(sys.argv[1:])




