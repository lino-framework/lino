# coding: latin1

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

import os
import types
from lino.misc.tsttools import TestCase, main

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *

from lino.reports import Report, RIGHT


examplesDir=os.path.join(os.path.dirname(__file__),
                         "..","..",
                         "docs","examples")

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.sess = demo.startup(self.ui)

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):


        for dirpath, dirnames, filenames in os.walk(examplesDir):
            for filename in filenames:
                base,ext = os.path.splitext(filename)
                if ext == '.py':
                    cmd="python "+os.path.join(examplesDir,filename)
                    fd=os.popen(cmd,"r")
                    observed=fd.read()
                    self.assertEqual(fd.close(),None)
                    outfile=os.path.join(examplesDir,base)+".out"
                    expected=open(outfile).read()
                    self.assertEquivalent(observed,expected,
                                          "Example %s failed"%filename)
        
        
##         self.sess.setBabelLangs('en')
        
##         rpt=Report(self.sess.schema.getTableList())
##         def onEach(row):
##             row.count=len(self.sess.query(row.item.__class__))
##         rpt.onEach(onEach)
        
##         rpt.addColumn(
##             meth=lambda row: row.item.getTableName(),
##             label="TableName",
##             width=20)
##         rpt.addColumn(
##             meth=lambda row: row.count,
##             width=5, halign=RIGHT,
##             label="Count")
##         rpt.addColumn(
##             meth=lambda row: self.sess.query(row.item.__class__)[0],
##             when=lambda row: row.count>0,
##             label="First",
##             width=20)
##         rpt.addColumn(
##             meth=lambda row: self.sess.query(row.item.__class__)[-1],
##             when=lambda row: row.count>0,
##             label="Last",
##             width=20)

##         self.ui.report(rpt)
##         s = self.getConsoleOutput()
##         print s
##         self.assertEquivalent(s,"""\
## TableName           |Count|First               |Last                
## --------------------+-----+--------------------+--------------------
## Languages           |    5|English             |Dutch               
## Users               |    2|Luc Saffre          |James Bond          
## Currencies          |    3|EUR                 |USD                 
## Nations             |    5|Estonia             |United States of    
##                     |     |                    |America             
## Cities              |   26|Bruxelles (be)      |Alfter-Oedekoven    
##                     |     |                    |(de)                
## Organisations       |    0|                    |                    
## Partners            |   12|Luc Saffre          |Eesti Telefon       
## PartnerTypes        |    5|Customer            |Sponsor             
## Events              |    0|                    |                    
## EventTypes          |    0|                    |                    
## Journals            |    1|outgoing invoices   |outgoing invoices   
## Years               |    0|                    |                    
## Products            |    2|(3,)                |(16,)               
## Invoices            |    1|OUT-1               |OUT-1               
## InvoiceLines        |    2|(u'OUT', 1, 1)      |(u'OUT', 1, 2)      
## Bookings            |    0|                    |                    
## Authors             |   14|Bill Gates          |Winston Churchill   
## AuthorEvents        |    0|                    |                    
## AuthorEventTypes    |    5|born                |other               
## Topics              |    0|                    |                    
## Publications        |    0|                    |                    
## Quotes              |    9|[q1]                |[q9]                
## PubTypes            |    6|Book                |Software            
## PubByAuth           |    0|                    |                    
## Pages               |    0|                    |                    
## Projects            |   10|Project 1           |Project 1.3.2.2     
## ProjectStati        |    5|to do               |sleeping            
## News                |    0|                    |                    
## Newsgroups          |    0|                    |                    
## """)        
        
            

if __name__ == '__main__':
    main()

