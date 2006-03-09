## Copyright 2003-2006 Luc Saffre
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

from lino.forms import Form

class DbMainForm(Form):

    def __init__(self,toolkit,dbc,*args,**kw):
        self.dbc=dbc
        Form.__init__(self,toolkit,*args,**kw)

    def addProgramMenu(self):
        m = self.addMenu("app","&Programm")
        m.addItem("logout",label="&Beenden",
                  action=self.close)
        m.addItem("about",label="Inf&o").setHandler(
            lambda : self.dbc.message(
            self.dbc.app.aboutString(), title="About"))

        def bugdemo(task):
            for i in range(5,0,-1):
                self.status("%d seconds left",i)
                task.increment()
                task.sleep()
            thisWontWork()
            
        
        m.addItem("bug",label="&Bug demo").setHandler(
            self.dbc.app.loop,bugdemo,"Bug demo")
        #m.addItem(label="show &Console").setHandler(self.showConsole)
        return m
    
    def addReportItem(self,*args,**kw):
        return self.dbc.addReportItem(*args,**kw)
    
    def onClose(self):
        self.dbc.close()

    def getTitle(self):
        return str(self.dbc)
    

