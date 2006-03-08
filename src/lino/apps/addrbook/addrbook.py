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

from lino.adamo.ddl import Schema, DbSession
from lino.forms import MainForm
#from lino.console import Application

from lino.apps.addrbook.tables import *

class MySchema(Schema):
    tableClasses = ( Language,
                     Nation, City,
                     Organisation, Person,
                     Partner, PartnerType)
    
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
        m.addReportItem("nations",NationsReport,label="&Nations")
        m.addReportItem("cities",CitiesReport,label="&Cities")
        m.addReportItem("partners",PartnersReport,label="&Partners")
        m.addReportItem("persons",PersonsReport,label="&Persons")
        
        self.addProgramMenu()
    
class AddressBook(DbSession):

    def run(self):
        MyMainForm(self).show()
    
        
    
