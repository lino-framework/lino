#coding: latin1

## Copyright 2005-2007 Luc Saffre 

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


from lino.adamo.ddl import *

from lino.apps.contacts import contacts_tables as contacts
from lino.apps.contacts.contacts_tables import Language
from lino.apps.contacts.contacts_tables import City, Nation
from lino.apps.contacts.contacts_tables import Organisation, Person
from lino.apps.contacts.contacts_tables import Contact, Function

from lino.apps.contacts.contacts_tables import \
     Contacts, ContactsMainForm

#from lino.i18n import BabelString


class Currency(BabelRow):
    
    tableName="Currencies"
    #tableLabel=BabelString("Currencies",de="Währungen",fr="Devises")
    
    def initTable(self,table):
        table.addField('id',ASTRING(width=3))
        BabelRow.initTable(self,table)
        
    def getLabel(self):
        return self.id

class CurrenciesReport(DataReport):
    leadTable=Currency

class Contact(contacts.Contact):
    # no tableName because this overrides contacts.Partner
    def initTable(self,table):
        contacts.Contact.initTable(self,table)
        table.addPointer('currency',Currency)


class Journal(StoredDataRow):
    tableName="Journals"
    def initTable(self,table):
        table.addField('id',ASTRING(width=3))
        table.addField('name',STRING).setMandatory()
        table.addField('tableName', ASTRING)
        
    def getLabel(self):
        return self.name
        
class JournalsReport(DataReport):
    leadTable=Journal




class Document(StoredDataRow):
    #abstract
    def initTable(self,table):
        table.addField('seq',ROWID)
        table.addField('date',DATE)
        table.addField('closed',BOOL)

        table.addPointer('jnl',Journal)#.setDetail("documents")
        table.setPrimaryKey("jnl seq")

    def getLabel(self):
        return self.jnl.id+"-"+str(self.seq)
        
        
class FinancialDocument(Document):
    def initTable(self,table):
        Document.initTable(self,table)
        table.addField('remark',STRING)
        
class BankStatement(FinancialDocument):
    tableName="BankStatements"
    def initTable(self,tbl):
        FinancialDocument.initTable(self,tbl)
        tbl.addField('balance1',AMOUNT)
        tbl.addField('balance2',AMOUNT)

class BankStatementsReport(DataReport):
    leadTable=BankStatement

        
class MiscOperation(FinancialDocument):
    tableName="MiscOperations"
    
class MiscOperationsReport(DataReport):
    leadTable=MiscOperation

class PartnerDocument(Document):
    def initTable(self,table):
        Document.initTable(self,table)
        table.addField('remark',STRING)
        table.addPointer('contact',Contact)

        

        


class Product(StoredDataRow):
    tableName="Products"
    def initTable(self,table):
        table.addField('id',ROWID)
        table.addField('name',STRING)
        table.addField('price',PRICE)
        
    def getLabel(self):
        return self.name


class ProductsReport(DataReport):
    leadTable=Product



class Invoice(PartnerDocument):
    tableName="Invoices"
    def initTable(self,table):
        PartnerDocument.initTable(self,table)
        table.addField('zziel',DATE)
        table.addField('amount',AMOUNT)
        table.addField('inverted',BOOL)
        #table.addPointer('partner',Partners).setDetail('invoices')
        #table.getRowAttr('partner')#.setDetail('invoices')
        table.addDetail('lines',InvoiceLine,'invoice')

    def close(self):
        #print "Invoices.close() : %s lines" % len(self.lines)
        self.lock()
        total = 0
        for line in self.lines():
            total += line.amount
        self.amount = total
        self.unlock()
        
##     def lines(self,*args,**kw):
##         kw['invoice']=self
##         return self.detail(InvoiceLine,*args,**kw)
    
class InvoicesReport(DataReport):
    leadTable=Invoice


class InvoiceLine(StoredDataRow):
    tableName="InvoiceLines"
    def initTable(self,table):
        table.addField('line',ROWID)
        table.addField('amount',AMOUNT)
        table.addField('remark',STRING)
        
        table.addPointer('invoice',Invoice)#.setDetail('lines')
        
        table.setPrimaryKey("invoice line")

class ProductInvoiceLine(InvoiceLine):
    
    def initTable(self,table):
        InvoiceLine.initTable(self,table)
        table.addField('unitPrice',AMOUNT)
        table.addField('qty',INT)
        table.addPointer('product',Product)
        #.setDetail('invoiceLines')
        
    def after_product(self):
        if self.product is None: return
        self.unitPrice = self.product.price
        if self.qty is None:
            self.qty = 1
        self.amount = self.unitPrice * self.qty
        #print self.amount



class InvoiceContentReport(DataReport):
    leadTable=InvoiceLine
    masterColumns="invoice"



    



class StatementItem(BabelRow):
    #abstract
    def initTable(self,table):
        BabelRow.initTable(self,table)
        table.addField('id',ASTRING)
        table.addField('attrib',STRING)
        table.addField('dc',STRING(1))
        table.addField('type',STRING(2))
        table.addField('doc',MEMO)
        #table.setPrimaryKey("stmt id")

class BalanceItem(StatementItem):
    """
    "Balance Sheet", "Bilanz", "Balance", "Bilanss"
    
    In formal bookkeeping and accounting, a balance sheet is a
    statement of the financial value (or "worth") of a business or
    other organisation (or person) at a particular date, usually at
    the end of its "fiscal year," as distinct from a profit and loss
    statement ("P&L," also known as an income statement), which
    records income and expenditures over some period. Therefore a
    balance sheet is often described as a "snapshot" of the company's
    financial condition at that time. Of the four basic financial
    statements, the balance sheet is the only statement which applies
    to a single point in time, instead of a period of time.

    The balance sheet has two parts: assets on the left-hand ("debit")
    side or at the top and liabilities on the right-hand ("credit")
    side or at the bottom. The assets of the company -- money ("in
    hand" or owed to it), investments (including securities and real
    estate), and other property -- are equal to the claims for
    payments of the persons or organisations owed -- the creditors,
    lenders, and shareholders. This standard format for balance sheets
    is derived from the principle of double-entry bookeeping.

    (Source: [url http://en.wikipedia.org/wiki/Balance_sheet])
"""
    
    tableName="BalanceItems"
    #pass

class BalanceReport(DataReport):
    leadTable=BalanceItem

class ProfitAndLossItem(StatementItem):
    """
    "Profit and loss account",
    "Gewinn- und Verlustrechnung",
    "Comptes de résultats",
    "Kasumiaruanne"),
            
A profit and loss account is a financial statement that summarizes the
financial transactions for a business over a period in time. In
reference to charitable organisations it is sometimes known as an
Income and Expenditure account.

Source: [url http://en.wikipedia.org/wiki/Profit_and_loss_statement]
    """
    tableName="ProfitAndLossItems"
    

class CashFlowItem(StatementItem):
    """

    "Cash flow statement",
    "",
    "",
    "Rahavoogude aruanne"),
            
A cash flow statement is a financial report that shows incoming and
outgoing money during a particular period (often monthly or
quarterly). It does not include non-cash items such as
depreciation. This makes it useful for determining the short-term
viability of a company, particularly its ability to pay bills.

Source: [url http://en.wikipedia.org/wiki/Cash_flow_statement]    
"""
    tableName="CashFlowItems"
    

        
class Account(BabelRow):
    tableName="Accounts"
    def initTable(self,table):
        BabelRow.initTable(self,table)
        #table.addField('label',STRING)
        table.addField('pcmn',STRING)
        table.addPointer('parent',Account)
        table.addPointer('balance',BalanceItem)
        table.addPointer('profit',ProfitAndLossItem)
        table.addPointer('cash',CashFlowItem)
        
class AccountsReport(DataReport):
    leadTable=Account
    
class Booking(StoredDataRow):
    tableName="Bookings"
    def initTable(self,table):
        table.addField('date',DATE)
        #table.addField('seq',ROWID)
        table.addField('amount',AMOUNT)
        table.addField('dc',BOOL)
        table.addPointer('account',Account)
        #table.addPointer('cr',Account)
        table.addField('label',STRING)
        
        table.addPointer('invoice',Invoice)
        table.addPointer('contact',Contact)
      
        #table.setPrimaryKey("date seq")
   
class BookingsReport(DataReport):
    leadTable=Booking
    



class LedgerSchema(contacts.ContactsSchema):
    
    tableClasses = (
        Currency,
        #Partner,
        Product,
        Journal,
        BankStatement, MiscOperation,
        Invoice, ProductInvoiceLine,
        BalanceItem,CashFlowItem,ProfitAndLossItem,
        Account,Booking,
        Language,
        Nation, City,
        Organisation, Person,
        Function, Contact, 
        #Partner,
        #PartnerType        
        ) #+ ContactsSchema.tableClasses


class LedgerMainForm(ContactsMainForm):
    """
    
Ledger is the general accounting suite that comes with Lino.
Ledger will be great, but it is not ready for use.


"""
    schemaClass=LedgerSchema
    def addLedgerMenu(self):
        m = self.addMenu("ledger","&Ledger")
        
        self.addReportItem(m,
            "products",ProductsReport,
            label="&Products")
        self.addReportItem(m,
            "gl",AccountsReport,
            label="&GL accounts")
        self.addReportItem(m,
            "ccy",CurrenciesReport,
            label="&Currencies")
        
        m = self.addMenu("sales","&Verkauf")
        self.addReportItem(
            m,
            "invoices",InvoicesReport,
            label="&Invoices")
        
    def setupMenu(self):
        self.addContactsMenu()
        self.addLedgerMenu()
        self.addProgramMenu()
    
    
class Ledger(Contacts):
    name="Lino Ledger"
    version="0.0.1"
    copyright="""\
Copyright (c) 2002-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://lino.saffre-rumma.ee/ledger.html"
    mainFormClass=LedgerMainForm
    
    
    
        
__all__ = [t.__name__ for t in LedgerSchema.tableClasses]
__all__.append('LedgerSchema')
__all__.append('Ledger')

## TABLES = (
##           Currency,
##           Language,
##           Nation, City,
##           Organisation, Person, 
##           Partner, PartnerType,
##           Product,
##           Journal,
##           BankStatement, MiscOperation,
##           Invoice, ProductInvoiceLine,
##           BalanceItem,CashFlowItem,ProfitAndLossItem,
##           Account,Booking
##           ) 

## __all__ = [t.__name__ for t in TABLES]
## __all__.append('TABLES')


