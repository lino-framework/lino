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
from lino.adamo.ddl import Schema

from lino.apps.spz import tables

class SPZ(Schema):
    name="Lino/SPZ"
    version="0.0.1"
    copyright="""\
Copyright (c) 2005 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    
    def setupSchema(self):
        for cl in tables.TABLES:
            self.addTable(cl)
    

    def showMainForm(self,sess):
        frm = sess.form(
            label="Main menu",
            doc="""\
This is the SPZ main menu.                                     
"""+("\n"*10))

        m = frm.addMenu("s","&Stammdaten")
        m.addItem("a",label="&Akten").setHandler(
            sess.showViewGrid, tables.Akten)
        
        self.addProgramMenu(sess,frm)

        frm.addOnClose(sess.close)

        frm.show()


if __name__ == '__main__':
    app=SPZ()
    app.quickStartup()
    gui.run(app)
