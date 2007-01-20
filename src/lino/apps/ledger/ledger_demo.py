# coding: latin1

## Copyright 2003-2007 Luc Saffre

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


import os, sys
#from lino import adamo
from lino.adamo.datatypes import itod
from lino.apps.contacts import contacts_demo as addrdemo
from ledger_tables import *
#from ledger_forms import Ledger


def startup(**kw):
    app=DemoLedger(**kw)
    return app.createContext()

class DemoLedger(Ledger):

    def __init__(self,
                 populate=True,big=False, withDemoData=True,
                 **kw):
        self.populate=populate
        self.big=big
        self.withDemoData=withDemoData
        Ledger.__init__(self,**kw)
    
    def createContext(self):
        ctx=Ledger.createContext(self)
        if self.populate:
            if self.withDemoData:
                self.runtask(DemoPopulator(big=self.big),ctx)
                #ctx.populate(DemoPopulator(big=self.big))
            else:
                self.runtask(StandardPopulator(big=self.big),ctx)
                #ctx.populate(StandardPopulator(big=self.big))
        return ctx
        




## def startup(filename=None, langs=None,
##             big=False,
##             dump=False,
##             populate=True,
##             withDemoData=True,
##             **kw):
##     schema = LedgerSchema(**kw)
##     sess=schema.quickStartup(langs=langs,
##                              filename=filename,
##                              dump=dump)

##     if populate:
##         if withDemoData:
##             sess.populate(DemoPopulator(big=big))
##         else:
##             sess.populate(StandardPopulator(big=big))

##     return sess


class StandardPopulator(addrdemo.StandardPopulator):

    def populateCurrencies(self,q):
        q.setBabelLangs('en de fr et')
        self.EUR = q.appendRow(
            id="EUR",
            name=("Euro","Euro","Euro","Euro"))
        self.BEF = q.appendRow(
            id="BEF",
            name=("Belgian Francs","Belgischer Franken",
                  "Franc belge","Belgia frank"))
        self.USD = q.appendRow(
            id="USD",
            name=("US Dollar","US-Dollar",
                  "Dollar US","USA dollar"))
        self.EEK = q.appendRow(
            id="EEK",name=("Estonian kroon","Estnische Krone",
                           "Couronne estonienne","Eesti kroon"))
    
    

##     def populateStatements(self,q):
##         q.setBabelLangs("en de fr ee")
##         self.balanceSheet=q.appendRow(
##             id="balanceSheet",
##             name=("Balance Sheet",
##                   "Bilanz",
##                   "Balance",
##                   "Bilanss"),
##             doc="""
## In formal bookkeeping and accounting, a balance sheet is a statement
## of the financial value (or "worth") of a business or other
## organisation (or person) at a particular date, usually at the end of
## its "fiscal year," as distinct from a profit and loss statement
## ("P&L," also known as an income statement), which records income and
## expenditures over some period. Therefore a balance sheet is often
## described as a "snapshot" of the company's financial condition at that
## time. Of the four basic financial statements, the balance sheet is the
## only statement which applies to a single point in time, instead of a
## period of time.

## The balance sheet has two parts: assets on the left-hand ("debit")
## side or at the top and liabilities on the right-hand ("credit") side
## or at the bottom. The assets of the company -- money ("in hand" or
## owed to it), investments (including securities and real estate), and
## other property -- are equal to the claims for payments of the persons
## or organisations owed -- the creditors, lenders, and
## shareholders. This standard format for balance sheets is derived from
## the principle of double-entry bookeeping.

## (Source: [url http://en.wikipedia.org/wiki/Balance_sheet])
##             """)
        
##         self.profitAndLoss=q.appendRow(
##             id="profitAndLoss",
##             name=("Profit and loss account",
##                   "Gewinn- und Verlustrechnung",
##                   "Comptes de résultats",
##                   "Kasumiaruanne"),
##             doc="""
            
## A profit and loss account is a financial statement that summarizes the
## financial transactions for a business over a period in time. In
## reference to charitable organisations it is sometimes known as an
## Income and Expenditure account.

## Source: [url http://en.wikipedia.org/wiki/Profit_and_loss_statement]

##             """)
        
##         self.cashFlow=q.appendRow(
##             id="cashFlow",
##             name=("Cash flow statement",
##                   "",
##                   "",
##                   "Rahavoogude aruanne"),
##             doc="""
            
## A cash flow statement is a financial report that shows incoming and
## outgoing money during a particular period (often monthly or
## quarterly). It does not include non-cash items such as
## depreciation. This makes it useful for determining the short-term
## viability of a company, particularly its ability to pay bills.


## Source: [url http://en.wikipedia.org/wiki/Cash_flow_statement]

##             """)
        
        
    def populateBalanceLines(self,q):
        #q.setBabelLangs("en de fr ee")
        # Bilans
        s=u"""\
1          Aktiva                                        
11         Käibevara                                      
1111       Raha ja pangakontod                            
1119       Ümmargused                                     
112        Nõuded ostjate vastu                           
1121       Ostjate tasumata arved                         
1122       Ebatõenäoliselt laekuvad arved (miinus)        
114        Mitmesugused nõuded                            
115        Ettemaks Tolliinspektuurile                    
116        Tulevaste perioodide kulud                     
1161       Maksude ettemaksed                             
1162       Muud nõuded (ebatõenäoliselt laekuvad arved)   
1163       Muud ettemakstud tulevaste perioodide kulud    
117        Varud                                          
1171       Ostetud kaubad müügiks                         
1172       Ettemaksed hankijatele                         
12         Põhivara                                       
121        Pikaajalised finantsinvesteeringud             
122        Materiaalne põhivara                           
1221       Masinad ja seadmed (soetusmaksumuses)          
1222       Akkumuleeritud põhivara kulum (-)             
"""
        #q.setBabelLangs("ee")
        for ln in s.splitlines():
            a=ln.split(None,1)
            assert len(a) == 2
            q.appendRow(id=str(a[0].strip()), name=a[1].strip(),dc="D")
            
        
        s=u"""\
2          PASSIVA (kohustused ja omakapital)            
21         Kohustused                                    
211        Lühiajalised kohustused                       
2111       Tagatiseta võlakohustused                     
2112       Hankijatele tasumata arved                    
2113       Maksuvõlad                                    
2114       Võlad töövõtjatele                            
2115       Muud lühiajalised võlgnevused                 
212        Pikaajalised kohustused                       
2121       Mittekonverteeritavad võlakohustused          
2122       Pangalaenud                                   
2123       Muud laenud                                   
22         Omakapital                                    
221        Osakapital                                    
222        Kohustuslik reserv                                    
223        Eelmiste perioodide jaotamata kasum (-kahjum) 
224        Aruandeperioodi kasum (-kahjum)               
"""                                                      
        for ln in s.splitlines():
            a=ln.split(None,1)
            assert len(a) == 2
            q.appendRow(id=str(a[0].strip()), name=a[1].strip(),dc="C")
            
    def populateProfitAndLossItems(self,q):
        q.setBabelLangs("en")
        # Kasumiaruanne
        s=u"""\
4          TULUD                       
41         Äritulud                    
411        Realiseerimise netokäive    
42         Finantstulud                
421        Intressitulud               
5          Ümmargused                  
6          KULUD                       
61         Ärikulud                    
610        Mitmesugused tegevuskulud   
611        Tööjõukulud                 
6111       Palgakulu                   
6112       Sotsiaal- jt. maksud        
612        Kulum ja allahindlus        
6121       Põhivara kulum              
613        Muud ärikulud               
62         Finantskulud
63         Ärikasum (-kahjum)
"""
        #print s.splitlines()
        for ln in s.splitlines():
            a=ln.split(None,1)
            assert len(a) == 2
            q.appendRow(id=str(a[0].strip()),
                        name=a[1].strip(),dc="C")

        # Rahavoogude aruanne
        """
1       Rahakäive äritegevusest : Cash flow from operations (CFO)
11        Tegevuskasum : Net income
12        Korrigeerimine kulumiga : Depreciation
13        Äritegevusega seotud nõuete muutus : Changes In Accounts Receivables
14        Lühiajaliste kohustuste muutus : Changes In Short-term Liabilities
15        Pikkajaliste kohustuste muutus : Changes In Long-term Liabilities

2       Rahakäive investeeringutest : Cash flow from investing (CFI)

        - Põhivara soetamine

3       Rahakäive finantseeringutest : Cash flow from financing (CFF)
        Raha ja pangakontod
        - perioodi lõpus
        - perioodi alguses
        """




class DemoPopulator(addrdemo.DemoPopulator,StandardPopulator):
    

    def populateContacts(self,q):
        addrdemo.DemoPopulator.populateContacts(self,q)
        #StandardPopulator.populateContacts(self,q)
        #q._store.commit()
        #return 
        NAT=q.getContext().query(Nation)
        #CCY=q.getContext().query(Currency)
        #BEF=CCY.peek("BEF")
        # must fetchall() because we update
        #for p in NAT.peek('be').contacts_by_nation().fetchall():
        #    p.update(currency=self.BEF)
        for p in NAT.peek('be').contacts_by_nation().fetchall():
            p.update(currency=self.BEF)

        # note: the Belgians will switch to EUR in tests/21.py
        
    def populateJournals(self,q):
        q = q.query("id name tableName")
        self.OUT = q.appendRow("OUT","outgoing invoices","INVOICES")
        
    def populateProducts(self,q):
        self.chair = q.appendRow(id=3,name="Chair",price=12)
        self.table = q.appendRow(id=16,name="Table",price=56)
        
    def populateInvoices(self,q):
        anton=q.getContext().query(
            Contact).findone(name="Anton Ausdemwald")
        self.invoice = q.appendRow(jnl=self.OUT,
                                   contact=anton,
                                   date=itod(20030822))
    def populateInvoiceLines(self,q):
        q.appendRow(invoice=self.invoice,product=self.chair,qty=4)
        q.appendRow(invoice=self.invoice,product=self.table,qty=1)

        
            
            
    
