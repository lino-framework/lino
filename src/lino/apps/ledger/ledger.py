#coding: latin1

## Copyright 2003-2005 Luc Saffre
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
from lino.apps.addrbook.addrbook import AddressBook
from lino.apps.ledger.tables import *


class Ledger(AddressBook):
    
    #tables=TABLES
    
    def setupSchema(self):
        self.addTable(Currency)
        AddressBook.setupSchema(self)
        for cl in (
            Partner,
            Product,
            Journal,
            BankStatement, MiscOperation,
            Invoice, ProductInvoiceLine,
            BalanceItem,CashFlowItem,ProfitAndLossItem,
            Account,Booking
          ):

            self.addTable(cl)
            
    
    def showMainForm(self,sess):
        frm = sess.form(
            label="Main menu",
            doc="""\
This is the Ledger main menu.                                    
"""+("\n"*10))

        m = frm.addMenu("ledger","&Ledger")
        m.addItem("products",label="&Products").setHandler(
            sess.showViewGrid, Product)
        m.addItem("gen",label="&GL accounts").setHandler(
            sess.showViewGrid, Account)
        m.addItem("ccy",label="&Currencies").setHandler(
            sess.showViewGrid, Currency)
        
        m = frm.addMenu("sales","&Verkauf")
        m.addItem("invoices",label="&Invoices").setHandler(
            sess.showViewGrid, Invoice)
        
        self.addProgramMenu(sess,frm)

        frm.addOnClose(sess.close)
        frm.show()



