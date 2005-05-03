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

import types
from lino.misc.tsttools import TestCase, main

from lino.adamo.rowattrs import Field, Detail

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *

from lino.reports import Report, RIGHT


class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.sess = demo.startup(self.ui,populate=False)

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        
        self.sess.setBabelLangs('en')
        
        rpt=Report(self.sess.schema.getTableList())
        
        rpt.addColumn(
            meth=lambda row: row.item.getTableName(),
            label="TableName",
            width=15)
        rpt.addColumn(
            meth=lambda row:\
            ", ".join([fld.name for fld in row.item.getFields()
                       if isinstance(fld,Field)]),
            label="Fields",
            width=25)
        rpt.addColumn(
            meth=lambda row:\
            ", ".join([fld.name for fld in row.item.getFields()
                       if isinstance(fld,Detail)]),
            label="Details",
            width=25)

        self.ui.report(rpt)
        s = self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""\
TableName      |Fields                   |Details                  
---------------+-------------------------+-------------------------
Languages      |id, name                 |partners_by_lang,        
               |                         |events_by_lang,          
               |                         |publications_by_lang,    
               |                         |quotes_by_lang,          
               |                         |pages_by_lang,           
               |                         |news_by_lang             
Users          |id, name, firstName, sex,|events_by_author,        
               |birthDate, id, password  |pages_by_author,         
               |                         |projects, newsByAuthor   
Currencies     |id, name                 |partners_by_currency     
Nations        |id, name, area,          |cities,                  
               |population, curr, isocode|organisations_by_nation, 
               |                         |partners_by_nation       
Cities         |id, name, zipCode,       |organisations_by_city,   
               |inhabitants              |partners_by_city,        
               |                         |authorevents_by_place    
Organisations  |id, email, phone, gsm,   |                         
               |fax, website, zip,       |                         
               |street, house, box, name |                         
Partners       |name, firstName, email,  |eventsByResponsible,     
               |phone, gsm, fax, website,|eventsByPlace, invoices, 
               |zip, street, house, box, |bookings_by_partner,     
               |id, title, logo          |projects_by_sponsor      
PartnerTypes   |id, name                 |partnersByType           
Events         |title, abstract, body,   |children, children,      
               |seq, id, created,        |news_by_page             
               |modified, match, id,     |                         
               |date, time               |                         
EventTypes     |title, abstract, body,   |eventsByType             
               |id, name                 |                         
Journals       |id, name, tableName      |documents                
Years          |id, name                 |                         
Products       |id, name, price          |invoiceLines             
Invoices       |seq, date, closed,       |lines,                   
               |remark, zziel, amount,   |bookings_by_invoice      
               |inverted                 |                         
InvoiceLines   |line, unitPrice, qty,    |                         
               |remark                   |                         
Bookings       |seq, date, amount, dc    |                         
Authors        |id, id, name, firstName, |authorevents_by_author,  
               |sex, birthDate           |publications_by_author,  
               |                         |quotesByAuthor,          
               |                         |pubbyauth_by_c           
AuthorEvents   |name, seq, date          |                         
AuthorEventType|name, id                 |authorevents_by_type     
s              |                         |                         
Topics         |seq, id, name, dewey,    |children                 
               |cdu, dmoz, wikipedia, url|                         
Publications   |title, abstract, body,   |children, pubbyauth_by_p 
               |seq, id, year, subtitle, |                         
               |typeRef                  |                         
Quotes         |title, abstract, body, id|                         
PubTypes       |id, name, typeRefPrefix, |publications_by_type     
               |pubRefLabel              |                         
PubByAuth      |                         |                         
Pages          |title, abstract, body,   |children, news_by_page   
               |seq, id, created,        |                         
               |modified, match          |                         
Projects       |title, abstract, body,   |children, news_by_project
               |seq, id, date, stopDate  |                         
ProjectStati   |name, id                 |projects                 
News           |title, abstract, body,   |                         
               |id, date                 |                         
Newsgroups     |id, name                 |newsByGroup              
""")        
        
            

if __name__ == '__main__':
    main()

