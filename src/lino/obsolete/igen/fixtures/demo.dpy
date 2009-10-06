#coding: utf8
## Copyright 2009 Luc Saffre

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

import time
from datetime import date
from dateutil import parser as dateparser
from lino.apps.igen.models import *
from lino.utils.instantiator import Instantiator
#from lino.plugins import journals

def i2d(i):
    return dateparser.parse(str(i))

#language_builder = Instantiator(Language,"id name")
journal = Instantiator(journals.Journal,"id name")
country_builder = Instantiator(Country,"isocode name")
shippingmode_builder = Instantiator(ShippingMode,"name")
paymentterm = Instantiator(PaymentTerm,"name").build

productcat = Instantiator(ProductCat,"name").build

contact_builder = Instantiator(Contact,fieldnames="""
      id
      firstName
      lastName
      title
      companyName
      nationalId
      vatId
      addr1
      addr2
      country
      city
      zipCode
      region
      email
      url
      phone
      gsm
      vatExempt
      itemVat
      language
      paymentTerm
      remarks
    """)
    
   


def objects():
    yield shippingmode_builder.build("cash and carry")
    yield shippingmode_builder.build("regular mail")

    yield paymentterm("Cash")
    yield paymentterm("7 days net",days=7)
    yield paymentterm("Prepayment",days=7)
    
    ORD = journals.create_journal("ORD",Order)
    yield ORD
    INV = journals.create_journal("INV",Invoice)
    yield INV    
    
    imode = Instantiator(InvoicingMode,
      "id channel name advance_days journal").build
    yield imode('e','E','By e-mail',2,"INV")
    yield imode('p','P','By snail mail',10,"INV")
        
    s = u"""    
    1||||Minu Firma OÜ|||||ee||||||||0|0|et|2|
    2|Luc|Saffre|Mr.||||Rummajaani talu|Vana-Vigala küla|ee|Vigala vald|78003|Raplamaa|luc.saffre@gmx.net||||0|0|et||
    3|Andreas|Arens|Herrn||||Vervierser Straße 12||be|Eupen|4700||||||0|0|de||
    4|Alfons|Ausdemwald|Herrn|Bäckerei Ausdemwald|||Vervierser Straße 45||be|Eupen|4700||||||0|0|de||
    5|Bernard|Bodard|Dr.||||rue de la Loi 17||be|Welkenraedt|4840||||||0|0|fr||
    6||||Donderweer bv|||Wolfgangamadeusplaats 1-5||nl|Sneek|8601 WB||||||0|0|nl||
    7|Jean|Dupont|Mr||||71, rue Neuve||fr|Prouvy|59121||||||0|0|fr||
    8|Emil|Eierschal|Herrn||||Eichenstr. 7||de|Erlangen|91056||||||0|0|de||
    9|Lisa|Lahm|Frau|Hans Flott & Co|||Dürener Str. 264-266||de|Aachen|52007||||||0|0|de||
    10|Bernd|Brecht|Herr|Bernd Brecht|||Eupener Str. 13||de|Aachen|52007||||||0|0|de||
    11|Jérôme|Jeanémart|Monsieur||||rue Haute||be|Welkenradt|4850||||||0|0|fr||
    12|Robin|Dubois|Monsieur||||rue des prés 5||be|Welkenradt|4850||||||0|0|fr||
    13|Denis|Duprez|Dr.||||rue des prés 9||be|Welkenradt|4850||||||0|0|fr||
    14|Karl|Keller|Herrn||||Bergstraße 5||be|Eupen|4700||||||0|0|de||
    100|Tõnu|Tamme||Mets ja Puu OÜ|||Sibula tee 1||ee|Maardu|74117|Harju|||||0|0|et||
    101|Karl|Kask|||||Nõmme tee 1|Kloogaranna küla|ee|Keila vald|76708|Harju|||||0|0|et||
    """

    for line in s.splitlines():
        if len(line.strip()) > 0:
            a = line.split('|')
            #print a
            yield contact_builder.build(*a)
        
        
    furniture = productcat("Furniture") #1
    yield furniture
    #print "foo", furniture.id, furniture
    yield productcat("Hosting") #2
    
    product = Instantiator(Product,"name price cat description").build
        
    yield product("Wooden table","199.99",1,"""\
This table is made of pure wood. 
<br/>It has <b>four legs</b>.
<br/>Designed to fit perfectly with <b>up to 6 wooden chairs</b>.
<br/>Product of the year 2008.
    """)
    yield product("Wooden chair","99.99",1,"")
    yield product("Metal table","129.99",1,"")
    yield product("Metal chair","79.99",1,"")
    hosting = product("Website hosting 1MB/month","3.99",2,"")
    yield hosting
    
    invoice = Instantiator(Invoice,
    "customer creation_date imode payment_term shipping_mode",journal=INV).build
    
    order = Instantiator(Order,
    """customer creation_date start_date cycle imode 
    payment_term shipping_mode""",journal=ORD).build
    
    #docitem = Instantiator(DocItem,"document product qty").build

    #~ o = ORD.create_document(
      #~ customer = Contacts.objects.get(pk=100),
      #~ creation_date = i2d(20080923),
      #~ start_date = i2d(20080924),
      #~ cycle = MONTHLY
    o = order(100,"2008-09-23","2008-09-24","M","e",2,1,
      remark="monthly order")
    o.add_item(hosting,1)
    yield o
    
    yield o.make_invoice(today=date(2008,10,28))
        
    i = invoice(2,"2008-10-29","e",2,1,remark="first manual invoice")
    i.add_item(1,1)
    i.add_item(2,4)
    yield i
    
    yield o.make_invoice(today=date(2009,04,11))
        
    i = invoice(3,date(2009,04,11),"e",2,1,
                remark="second manual invoice")
    i.add_item(3,1)
    i.add_item(4,4)
    yield i
    
    o2 = order(4,"2009-04-12","2009-04-12","Y","p",2,1,
               remark="yearly order")
    o2.add_item(3,1)
    o2.add_item(4,4)
    yield o2
    yield o2.make_invoice(today=date(2009,04,12))
    
    i = invoice(4,date(2009,04,12),"e",2,1,
      remark="third manual invoice with discount")
    i.add_item(3,1,discount=10)
    i.add_item(4,4,discount=5)
    yield i
    
    yield o.make_invoice(today=date(2009,05,14))

    account = Instantiator(Account,"name").build
    
    BANK = journals.create_journal("BANK",FinancialDocument)
    yield BANK
    
    EL = account("Electricity")
    IN = account("Internet")
    CU = account("Customers")
    PR = account("Providers")
    
    doc = BANK.create_document(creation_date=i2d(20090501))
    doc.add_item(account=PR,contact=Contact.objects.get(pk=2),
      debit='12.49')

    yield doc