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
from lino.console.application import Application

from lino.apps.timings import Timings
from lino.apps.keeper import Keeper
        
class LinoDemo(Application):
    #name="Lino/Demo"
    years='2005'
    author="Luc Saffre"
    
    def showMainForm(self,sess):
        frm = sess.form(
            label="LinoDemo Main menu",
            doc="""\
This is the LinoDemo main menu.                                     
"""+("\n"*10))

        m = frm.addMenu("apps","&Applications")
        
        m.addItem("timings",label="&Timings").setHandler(
            sess.runTask, Timings)
        
        m.addItem("keeper",label="&Keeper").setHandler(
            sess.runTask, Keeper)
        
        self.addProgramMenu(sess,frm)

        frm.addOnClose(sess.close)

        frm.show()


if __name__ == '__main__':
    sess=LinoDemo().startup()
    gui.run(sess)
