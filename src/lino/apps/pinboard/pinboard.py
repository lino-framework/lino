#coding: iso-8859-1
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

from lino.apps.pinboard import tables 
from lino.adamo.ddl import Schema

from lino.gendoc.html import HtmlDocument
from lino.reports.reports import DataReport


class Pinboard(Schema):
    name="Lino/Pinboard"
    years='2005'
    author="Luc Saffre"
    
    
    def setupSchema(self):
        for cl in tables.TABLES:
            self.addTable(cl)
    

    def showMainForm(self,sess):
        frm = sess.form(
            label="Main menu",
            doc="""\
This is the Pinboard main menu.                                     
"""+("\n"*10))

        m = frm.addMenu("db","&Datenbank")
        m.addItem("authors",label="&Authors").setHandler(
            sess.showViewGrid, tables.Author)
        m.addItem("nodes",label="&Nodes").setHandler(
            sess.showViewGrid, tables.Node)
        m.addItem("news",label="&News").setHandler(
            sess.showViewGrid, tables.NewsItem)
        m.addItem("newsgroups",label="News&groups").setHandler(
            sess.showViewGrid, tables.Newsgroup)
        
##         m = frm.addMenu("reports","&Reports")
##         m.addItem("s",label="&Static HTML").setHandler(
##             self.writeStaticSite,sess)
        
        self.addProgramMenu(sess,frm)

        frm.addOnClose(sess.close)

        frm.show()


if __name__ == '__main__':
    app=Pinboard()
    app.quickStartup()
    #app.main()
    gui.run(app)
