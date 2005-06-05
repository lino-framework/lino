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

from lino.apps.timings.tables import *
from lino.apps.timings.tables import TABLES
from lino.adamo.ddl import Schema

from lino.gendoc.html import HtmlDocument
from lino.reports.reports import DataReport


class Pinboard(Schema):
    #name="Lino/Timings"
    years='2005'
    author="Luc Saffre"
    
    tables = TABLES

    def showMainForm(self,sess):
        frm = sess.form(
            label="Main menu",
            doc="""\
This is the Timings main menu.                                     
"""+("\n"*10))

        m = frm.addMenu("db","&Datenbank")
        m.addItem("authors",label="&Authors").setHandler(
            sess.showTableGrid, Authors)
        m.addItem("pages",label="&Pages").setHandler(
            sess.showTableGrid, Pages)
        m.addItem("usageTypes",label="Usage &Types").setHandler(
            sess.showTableGrid, UsageTypes)
        
        m = frm.addMenu("reports","&Reports")
        m.addItem("s",label="&Static HTML").setHandler(
            self.writeStaticSite,sess)
        
        self.addProgramMenu(sess,frm)

        frm.addOnClose(sess.close)

        frm.show()


if __name__ == '__main__':
    app=Timings()
    app.quickStartup()
    #app.main()
    gui.run(app)
