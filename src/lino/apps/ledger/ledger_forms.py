#coding: latin1

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

#from lino.adamo.ddl import Schema

from lino.apps.contacts.contacts_data import Contacts
from ledger_data import *

class LedgerMainForm(ContactsMainForm):
    """
    
This is the Ledger main menu.


"""
    def setupLedgerMenu(self):
        m = self.addMenu("ledger","&Ledger")
        
        self.addReportItem(m,
            "products",tables.ProductsReport,
            label="&Products")
        self.addReportItem(m,
            "gl",tables.AccountsReport,
            label="&GL accounts")
        self.addReportItem(m,
            "ccy",tables.CurrenciesReport,
            label="&Currencies")
        
        m = self.addMenu("sales","&Verkauf")
        self.addReportItem(
            m,
            "invoices",tables.InvoicesReport,
            label="&Invoices")
        
    def setupMenu(self):
        self.addContactsMenu()
        self.addLedgerMenu()
        self.addProgramMenu()
    
    
class Ledger(Contacts):
    version="0.0.1"
    copyright="""\
Copyright (c) 2002-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://lino.saffre-rumma.ee/ledger.html"
    schemaClass=LedgerSchema
    mainFormClass=LedgerMainForm
    
##     def setupSchema(self):
##         self.addTable(Currency)
##         AddressBook.setupSchema(self)
##         for cl in (
##             Partner,
##             Product,
##             Journal,
##             BankStatement, MiscOperation,
##             Invoice, ProductInvoiceLine,
##             BalanceItem,CashFlowItem,ProfitAndLossItem,
##             Account,Booking
##           ):

##             self.addTable(cl)
            
    



