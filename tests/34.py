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

"""

This is to test whether the schema of each application initializes
correctly.

see also :
test 81 does a demo.startup() of all these applications

"""

from lino.misc.tsttools import TestCase, main
from lino.adamo.dbreports import DatabaseOverview, SchemaOverview
from lino.apps.contacts.pinboard_forms import Pinboard
from lino.apps.contacts.contacts_forms import Contacts
from lino.apps.keeper.keeper_forms import Keeper
from lino.apps.ledger.ledger_forms import Ledger


class Case(TestCase):

    
    def test01(self):
        app = Contacts()
        SchemaOverview(app.dbsess.db.schema).show()
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""\
TableName      |Fields              |Pointers     |Details             
---------------+--------------------+-------------+--------------------
Languages      |id, name            |             |                    
Nations        |id, name, area,     |             |cities,             
               |population, curr,   |             |partners_by_nation  
               |isocode             |             |                    
Cities         |id, name, zipCode,  |nation       |                    
               |inhabitants         |             |                    
Organisations  |id, email, phone,   |nation, city |                    
               |gsm, fax, website,  |             |                    
               |zip, street, house, |             |                    
               |box, name           |             |                    
Persons        |id, name, firstName,|             |                    
               |sex, birthDate      |             |                    
Partners       |name, firstName,    |nation, city,|                    
               |email, phone, gsm,  |type, lang   |                    
               |fax, website, zip,  |             |                    
               |street, house, box, |             |                    
               |id, title, logo     |             |                    
PartnerTypes   |id, name            |             |                    
        """)
        
        DatabaseOverview(app.dbsess).show()
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""\
TableName           |Count|First               |Last
--------------------+-----+--------------------+--------------------
Languages           |    0|                    |
Nations             |    0|                    |
Cities              |    0|                    |
Organisations       |    0|                    |
Persons             |    0|                    |
Partners            |    0|                    |
PartnerTypes        |    0|                    |
""")
        #app.main()
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""\
        """)
        app.close()
        
    def test02(self):
        app = Keeper()
        SchemaOverview(app.dbsess.db.schema).show()
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""
TableName      |Fields              |Pointers     |Details
---------------+--------------------+-------------+--------------------
Volumes        |id, name, meta, path|             |directories
Files          |name, mtime, size,  |dir, type    |occurences
               |content, meta,      |             |
               |mustParse           |             |
Directories    |id, name, meta      |parent,      |files, subdirs
               |                    |volume       |
FileTypes      |id, name            |             |
Words          |id                  |synonym      |occurences
Occurences     |pos                 |word, file   |
        """)
        DatabaseOverview(app.dbsess).show()
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""
TableName           |Count|First               |Last
--------------------+-----+--------------------+--------------------
Volumes             |    0|                    |
Files               |    0|                    |
Directories         |    0|                    |
FileTypes           |    0|                    |
Words               |    0|                    |
Occurences          |    0|                    |        
        """)
        app.close()
        
        
    def test03(self):
        app = Ledger()
        SchemaOverview(app.dbsess.db.schema).show()
        s=self.getConsoleOutput()
        # print s
        self.assertEquivalent(s,"""
TableName      |Fields              |Pointers     |Details
---------------+--------------------+-------------+--------------------
Currencies     |id, name            |             |
Products       |id, name, price     |             |
Journals       |id, name, tableName |             |
BankStatements |seq, date, closed,  |jnl          |
               |remark, balance1,   |             |
               |balance2            |             |
MiscOperations |seq, date, closed,  |jnl          |
               |remark              |             |
Invoices       |seq, date, closed,  |jnl, partner |lines
               |remark, zziel,      |             |
               |amount, inverted    |             |
InvoiceLines   |line, amount,       |invoice,     |
               |remark, unitPrice,  |product      |
               |qty                 |             |
BalanceItems   |name, id, attrib,   |             |
               |dc, type, doc       |             |
CashFlowItems  |name, id, attrib,   |             |
               |dc, type, doc       |             |
ProfitAndLossIt|name, id, attrib,   |             |
ems            |dc, type, doc       |             |
Accounts       |name, pcmn, id      |parent,      |
               |                    |balance,     |
               |                    |profit, cash |
Bookings       |date, amount, dc,   |account,     |
               |label, id           |invoice,     |
               |                    |partner      |
Languages      |id, name            |             |
Nations        |id, name, area,     |             |cities,
               |population, curr,   |             |partners_by_nation
               |isocode             |             |
Cities         |id, name, zipCode,  |nation       |
               |inhabitants         |             |
Organisations  |id, email, phone,   |nation, city |
               |gsm, fax, website,  |             |
               |zip, street, house, |             |
               |box, name           |             |
Persons        |id, name, firstName,|             |
               |sex, birthDate      |             |
Partners       |name, firstName,    |nation, city,|
               |email, phone, gsm,  |type, lang,  |
               |fax, website, zip,  |currency     |
               |street, house, box, |             |
               |id, title, logo     |             |
PartnerTypes   |id, name            |             |        
        """)
        DatabaseOverview(app.dbsess).show()
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""
TableName           |Count|First               |Last                
--------------------+-----+--------------------+--------------------
Currencies          |    0|                    |                    
Products            |    0|                    |                    
Journals            |    0|                    |                    
BankStatements      |    0|                    |                    
MiscOperations      |    0|                    |                    
Invoices            |    0|                    |                    
InvoiceLines        |    0|                    |                    
BalanceItems        |    0|                    |                    
CashFlowItems       |    0|                    |                    
ProfitAndLossItems  |    0|                    |                    
Accounts            |    0|                    |                    
Bookings            |    0|                    |                    
Languages           |    0|                    |                    
Nations             |    0|                    |                    
Cities              |    0|                    |                    
Organisations       |    0|                    |                    
Persons             |    0|                    |                    
Partners            |    0|                    |                    
PartnerTypes        |    0|                    |                    
        """)
        app.close()
        
        

if __name__ == '__main__':
    main()

