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
opj = os.path.join

from lino import adamo
from lino.forms import gui

from lino.apps.keeper import keeper_tables as tables
#from lino.apps.keeper.populate import Populator

from lino.forms.application import AdamoApplication

class Keeper(AdamoApplication):
        
    def makeMainForm(self,ui):
        frm = ui.form(
            label="Main menu",
            doc="""\
This is the Keeper main menu.                                     
"""+("\n"*10))

        m = frm.addMenu("&Stammdaten")
        m.addItem(label="&Volumes").setHandler(
            self.showTableGrid,ui,
            tables.Volumes,viewName="std")
        m.addItem(label="&Files").setHandler(
            self.showTableGrid,ui,
            tables.Files,viewName="std")
        m.addItem(label="&Directories").setHandler(
            self.showTableGrid,ui,
            tables.Directories,viewName="std")
        m.addItem(label="&Words").setHandler(
            self.showTableGrid,ui,
            tables.Words)
    
##         m = frm.addMenu("&Load")
##         m.addItem(label="&Path").setHandler(
##             self.loadPath,ui)
        
        m = frm.addMenu("&Programm")
        m.addItem(label="&Beenden",action=frm.close)
        m.addItem(label="Inf&o").setHandler(ui.showAbout,self)

        return frm

##     def loadPath(self,ui):
##         path = r'c:\temp\1'
##         p = Populator(self.sess)
##         p.visit(path,"")

def main(argv):

    app = Keeper(name="Keeper", years='2005')
    app.parse_args()
    tables.setupSchema(app.schema)
    gui.run(app)
    




if __name__ == '__main__':
    main(sys.argv[1:])




