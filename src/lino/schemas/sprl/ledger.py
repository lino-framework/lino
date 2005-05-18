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

from lino.adamo import *

#from lino.adamo.table import Table
#from lino.adamo.datatypes import *
from addrbook import Partners
from sales import Invoices

## class Statements(BabelTable):
##     def init(self):
##         self.addField('id',STRING)
##         BabelTable.init(self)
##         self.addField('doc',MEMO)

        
class StatementItems(BabelTable):
    
    def init(self):
        BabelTable.init(self)
        self.addField('id',STRING)
        self.addField('attrib',STRING)
        self.addField('filter',STRING)
        self.addField('doc',MEMO)
        #self.setPrimaryKey("stmt id")

class BalanceItems(StatementItems):
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
    
    #pass

class ProfitAndLossItems(StatementItems):
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
    #pass

class CashFlowItems(StatementItems):
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
    pass

        
class Accounts(BabelTable):
    def init(self):
        BabelTable.init(self)
        #self.addField('label',STRING)
        self.addField('pcmn',STRING)
        self.addPointer('parent',Account)
        self.addPointer('balance',BalanceItems)
        self.addPointer('profit',ProfitAndLossItems)
        self.addPointer('cash',CashFlowItems)
        
class Bookings(Table):
    def init(self):
        self.addField('date',DATE)
        #self.addField('seq',ROWID)
        self.addField('amount',AMOUNT)
        #self.addField('dc',BOOL)
        self.addPointer('db',Accounts)
        self.addPointer('cr',Accounts)
        self.addField('label',STRING)
        
        self.addPointer('invoice',Invoices)
        self.addPointer('partner',Partners)
      
        #self.setPrimaryKey("date seq")
   
