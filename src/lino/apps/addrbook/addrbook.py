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

from lino.adamo.ddl import Schema, DbApplication
from lino.forms import MainForm
#from lino.console import Application

from lino.apps.addrbook.tables import *

## class MySchema(Schema):
    
##     def setupSchema(self):
##         for cl in ( Language,
##                     Nation, City,
##                     Organisation, Person,
##                     Partner, PartnerType):
##             self.addTable(cl)

class MyMainForm(MainForm):
    """Welcome to AddressBook, a Lino Application for
    demonstration purposes."""

    def setupMenu(self):
        m = self.addMenu("master","&Master")
        self.addReportItem(
            m,"nations",NationsReport,label="&Nations")
        self.addReportItem(
            m,"cities",CitiesReport,label="&Cities")
        self.addReportItem(
            m,"partners",PartnersReport,label="&Partners")
        self.addReportItem(
            m,"persons",PersonsReport,label="&Persons")
        
        self.addProgramMenu()
    
class AddressBook(DbApplication):
    tableClasses = ( Language,
                     Nation, City,
                     Organisation, Person,
                     Partner, PartnerType)

    def run(self,dbc=None):
        if dbc is None:
            dbc=self.quickStartup()
        MyMainForm(self.toolkit,dbc).show()
    
        
    
