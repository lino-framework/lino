# coding: latin1

## Copyright Luc Saffre 2003-2005

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

"""
"""


import os
from lino import adamo
#from lino.schemas.sprl.sprl import makeSchema
#from lino.schemas.sprl import tables 
from lino.tools.normalDate import ND
from lino.adamo.datatypes import itod
#from lino.ui import console
from lino.schemas.sprl.sprl import Sprl

## class DemoSprl(Sprl):

##     def __init__(self,
##                  populate=True,
##                  big=False,
##                  withDemoData=True,
##                  withJokes=False,
##                  **kw):
##         Sprl.__init__(self,**kw)
##         #self.big=big
##         #self.withDemoData=withDemoData
##         #self.withJokes=withJokes
##         if populate:
##             if withJokes:
##                 self.addPopulator(JokesPopulator(big=big,
##                                                  label="Weisheiten"))
##             elif withDemoData:
##                 self.addPopulator(DemoPopulator(big=big,
##                                                   label="StandardDemo"))
##             else:
##                 self.addPopulator(Populator(big=big,
##                                             label="Standard"))


## def makeSchema(populate=True,
##                big=False,
##                withDemoData=True,
##                withJokes=False,
##                **kw):
##     schema = sprl.makeSchema(**kw)
##     if populate:
##         if withJokes:
##             schema.addPopulator(JokesPopulator(big=big,
##                                                label="Weisheiten"))
##         elif withDemoData:
##             schema.addPopulator(DemoPopulator(big=big,
##                                               label="StandardDemo"))
##         else:
##             schema.addPopulator(Populator(big=big,
##                                           label="Standard"))
##     return schema
            
            
def startup(filename=None, langs=None,
            populate=True,
            big=False,
            withDemoData=True,
            **kw):
    schema = Sprl(**kw)
    #if ui is None:
    #    ui = console.getSystemConsole()
    sess=schema.quickStartup(langs=langs, filename=filename)
    if populate:
        if withDemoData:
            sess.populate(DemoPopulator(big=big,
                                        label="StandardDemo"))
        else:
            sess.populate(Populator(big=big,
                                    label="Standard"))

    return sess


# deprecated name for startup:
beginSession = startup




class Populator(adamo.Populator):
    def __init__(self,
                 big=False,**kw
                 #withDemoData=False,
                 #withJokes=False,
                 ):
        self.big = big
        adamo.Populator.__init__(self,None,**kw)
        #self.withDemoData = withDemoData
        #self.withJokes = withJokes
        
    def populateUsers(self,q):
        q = q.child('id firstName name')
        q.appendRow("luc", "Luc", "Saffre")
        q.appendRow("james", "James", "Bond")
        
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
    
    def populatePartnerTypes(self,q):
        q = q.query('id name')
        q.setBabelLangs('en de fr')
        q.appendRow('c',('Customer', 'Kunde', 'Client'))
        q.appendRow('s',('Supplier', 'Lieferant', 'Fournisseur'))
        q.appendRow('m',('Member', 'Mitglied', "Membre"))
        q.appendRow('e',('Employee', 'Angestellter', "Employé"))
        q.appendRow('d',('Sponsor', 'Sponsor', "Sponsor"))
	
        
    
    def populateNations(self,q):
        if self.big:
            from lino.schemas.sprl.data import nations
            nations.populate(q)
            if q.getDatabase().supportsLang("de"):
                from lino.schemas.sprl.data import nations_de
                nations_de.populate(q)
            
        else:
            q = q.query('id name cities')
            q.setBabelLangs('en')
            q.appendRow("ee","Estonia")
            q.appendRow("be","Belgium")
            q.appendRow("de","Germany")
            q.appendRow("fr","France")
            q.appendRow("us","United States of America")

        self.belgique = q.peek('be')
        self.eesti = q.peek('ee')
        self.deutschland = q.peek('de')

    
    def populateCities(self,q):
        if self.big:
            from lino.schemas.sprl.data import cities_de
            cities_de.populate(q)
            from lino.schemas.sprl.data import cities_be
            cities_be.populate(q)
        else:
            q = self.belgique.cities.query('name inhabitants')
            q.appendRow("Bruxelles",1004239)
            q.appendRow("Brugge",116848)
            q.appendRow("Eupen",17872)
            #q.appendRow("Kettenis")
            q.appendRow("Kelmis",10175)
            q.appendRow("Raeren",9933)
            q.appendRow("Mons",90992)
            q.appendRow("Liège",185608)
            q.appendRow("Charleroi",200983)
            q.appendRow("Verviers",52739)

        self.eupen = q.findone(name="Eupen")
        self.verviers = q.findone(name="Verviers")
            
        q = q.query('name inhabitants', nation=self.eesti)
        self.tallinn = q.appendRow("Tallinn",442000)
##         assert tallinn.inhabitants == 442000
##         assert tallinn.nation == self.eesti
##         assert tallinn.nation.id == "ee"
##         assert tallinn.getRowId() == ['ee',1], \
##                  "%s != ['ee',1]" % repr(tallinn.getRowId())

        q.appendRow("Tartu",109100)
        #q.appendRow("Otepää")
        q.appendRow("Narva",80300)
        q.appendRow("Kilingi-Nõmme",2490)
        q.appendRow("Pärnu",52000)
        q.appendRow("Rakvere",18096)
        q.appendRow("Viljandi",20756)
        q.appendRow("Ruhnu",58)
        q.appendRow("Vigala",1858)
        q.appendRow("Kohtla-Järve",70800)

        q = self.deutschland.cities.query('name') 
        self.aachen = q.appendRow("Aachen")
        q.appendRow("Köln")
        q.appendRow("Berlin")
        q.appendRow("Bonn")
        q.appendRow("München")
        q.appendRow("Eschweiler")
        q.appendRow("Alfter-Oedekoven")
    

            


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
        s="""\
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
            q.appendRow(id=a[0].strip(), name=a[1].strip(),dc="D")
            
        
        s="""\
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
            q.appendRow(id=a[0].strip(), name=a[1].strip(),dc="C")
            
    def populateProfitAndLossItems(self,q):
        q.setBabelLangs("en")
        # Kasumiaruanne
        s="""\
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
            q.appendRow(id=a[0].strip(), name=a[1].strip(),dc="C")

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




class DemoPopulator(Populator):
    
        

    def populateJournals(self,q):
        q = q.query("id name tableName")
        self.OUT = q.appendRow("OUT","outgoing invoices","INVOICES")
        
    def populateProducts(self,q):
        self.chair = q.appendRow(id=3,name="Chair",price=12)
        self.table = q.appendRow(id=16,name="Table",price=56)
        
    def populateInvoices(self,q):
        self.invoice = q.appendRow(jnl=self.OUT,
                                   partner=self.anton,
                                   date=itod(20030822))
    def populateInvoiceLines(self,q):
        q.appendRow(invoice=self.invoice,product=self.chair,qty=4)
        q.appendRow(invoice=self.invoice,product=self.table,qty=1)

        
    def populatePartners(self,q):

##         tallinn = q.getSession().query(Cities).findone(
##             nation=self.eesti,
##             name="Tallinn")

##         # todo: eupen = belgique.cities.findone(name="Eupen")
##         eupen = q.getSession().query(Cities).findone(
##             nation=self.belgique,
##             name="Eupen")

##         verviers = q.getSession().query(Cities).findone(
##             nation=self.belgique,
##             name="Verviers")

##         aachen = q.getSession().query(Cities).findone(
##             nation=deutschland,
##             name="Aachen")


        q = q.query(
            'name firstName title email phone city currency')

        self.luc = q.appendRow(
            'Saffre','Luc','Herrn',
            'luc.saffre@gmx.net', '6376783', self.tallinn)
##         assert luc.id == 1 # "Saffre"
##         assert luc.name == 'Saffre'
##         assert luc.city == tallinn, \
##                  "%s != %s" % (repr(luc.city), repr(tallinn))

        #PARTNERS.flush()
        #luc = q.peek(1)
        #assert luc.id == 1 # "Saffre"
        #assert luc.name == 'Saffre'
        #assert luc.city == tallinn

        # fictive persons
        q.appendRow('Arens'   ,'Andreas'  , "Herrn",
                    'andreas@arens.be', '087.55.66.77',
                    self.eupen, self.BEF)
        self.anton = q.appendRow(
            'Ausdemwald','Anton'      , "Herrn",
            'ausdem@hotmail.com', None, self.aachen, self.EUR)
        q.appendRow('Bodard'      ,'Henri'    , "Dr.",
                    None, None,self.verviers, self.BEF)
        q.appendRow('Eierschal' ,'Emil'   , "Herrn",
                    None, None,self.eupen, self.EUR)
        q.appendRow('Eierschal' ,'Erna'   , "Frau",
                    None, None,self.eupen,self.EUR)
        q.appendRow('Großmann'  ,'Gerd'   , "Herrn",
                    None, None,self.eupen,self.EUR)
        q.appendRow('Freitag'     ,'Frédéric' , "Herrn",
                    None, None,self.eupen)

        q = q.query('name zip street house box city')

        rumma = q.appendRow(
            'Rumma & Ko OÜ','10115', 'Tartu mnt.','71','5',
            self.tallinn)
        girf = q.appendRow(
            'Girf OÜ','10621','Laki',"16", None, self.tallinn)
        pac = q.appendRow(
            'PAC Systems PGmbH','4700','Hütte',"79" , None, self.eupen)
        q.appendRow(
            'Eesti Telefon','13415','Sõpruse pst.',"193", None,
            self.tallinn)

        assert rumma.name == "Rumma & Ko OÜ"
        assert rumma.nation == self.eesti, \
               "%s != %s" % (repr(rumma.nation), repr(self.eesti))

            
            
    
