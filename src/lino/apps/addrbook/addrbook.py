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


from lino.apps.addrbook.addrbook_schema import *
from lino.forms import DbMainForm, DbApplication

class ContactsMainForm(DbMainForm):
    
    """\
Welcome to AddressBook, a Lino Forms Application for
demonstration purposes.
"""

    def setupContactsMenu(self):
        m = self.addMenu("contacts","&Contacts")
        self.addReportItem(
            m,"nations",NationsReport,label="&Nations")
        self.addReportItem(
            m,"cities",CitiesReport,label="&Cities")
        self.addReportItem(
            m,"partners",PartnersReport,label="&Partners")
        self.addReportItem(
            m,"orgs",OrganisationsReport,label="&Organisations")
        self.addReportItem(
            m,"persons",PersonsReport,label="&Persons")
        
    def setupMenu(self):
        self.setupContactsMenu()
        self.addProgramMenu()
    

class Contacts(DbApplication):
    name="Lino AdressBook"
    version="0.0.1"
    author="Luc Saffre"
    mainFormClass=ContactsMainForm
    schemaClass=ContactsSchema
