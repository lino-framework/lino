# coding: latin1

## Copyright Luc Saffre 2003-2005.

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

import types
import unittest

from lino.adamo.datatypes import DataVeto
from lino.adamo import Table

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *


class Case(unittest.TestCase):

    def setUp(self):
        
        self.sess = demo.beginSession()

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        
        self.sess.setBabelLangs('en')
        self.sess.startDump()
        
        rpt = self.sess.report()
        rpt.addColumn(
            meth=lambda rpt: rpt.crow.getTableName(),
            label="TableName",
            width=20)
        def count(rpt):
            return len(self.sess.query(rpt.crow.__class__))
        rpt.addColumn(
            meth=count,
            width=5, halign=rpt.RIGHT,
            label="Count")
        rpt.addColumn(
            meth=lambda rpt: self.sess.query(rpt.crow.__class__)[0],
            when=lambda rpt: rpt.cellValues[1]>0,
            label="First",
            width=20)
        rpt.addColumn(
            meth=lambda rpt: self.sess.query(rpt.crow.__class__)[-1],
            when=lambda rpt: rpt.cellValues[1]>0,
            label="Last",
            width=20)
        
        rpt.beginReport()
        for t in self.sess.schema.getTableList():
            rpt.processRow(t)
        rpt.endReport()
        s = self.sess.stopDump()
        # print s
        self.assertEqual(s,"""\
TableName           |Count|First               |Last                
--------------------+-----+--------------------+--------------------
Languages           |    5|English             |Dutch               
Users               |    2|Luc Saffre          |James Bond          
Nations             |    5|Estonia             |United States of    
                    |     |                    |America             
Cities              |   27|Bruxelles (be)      |Alfter-Oedekoven    
                    |     |                    |(de)                
Organisations       |    1|(1,)                |(1,)                
Partners            |   12|Luc Saffre          |Eesti Telefon       
PartnerTypes        |    5|Customer            |Sponsor             
Currencies          |    3|EUR                 |USD                 
Events              |    0|                    |                    
EventTypes          |    0|                    |                    
Journals            |    1|outgoing invoices   |outgoing invoices   
Years               |    0|                    |                    
Products            |    2|(3,)                |(16,)               
Invoices            |    1|OUT-1               |OUT-1               
InvoiceLines        |    2|('OUT', 1, 1)       |('OUT', 1, 2)       
Bookings            |    0|                    |                    
Authors             |   13|Bill Gates          |Henry Louis Mencken 
AuthorEvents        |    0|                    |                    
AuthorEventTypes    |    5|born                |other               
Topics              |    0|                    |                    
Publications        |    0|                    |                    
Quotes              |    8|[q1]                |[q8]                
PubTypes            |    6|Book                |Software            
PubByAuth           |    0|                    |                    
Pages               |    2|Lino Demo Data      |Bullshit Bingo      
Projects            |   10|Project 1           |Project 1.3.2.2     
ProjectStati        |    5|to do               |sleeping            
News                |    0|                    |                    
Newsgroups          |    0|                    |                    
""")        
        
            

if __name__ == '__main__':
    unittest.main()

