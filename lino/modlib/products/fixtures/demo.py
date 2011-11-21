# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

#from lino.apps.products.models import *
from lino import reports
products = reports.get_app('products')
from lino.utils.instantiator import Instantiator

from lino.utils.babel import babel_values, default_language


productcat = Instantiator('products.ProductCat').build
product = Instantiator('products.Product',"price cat").build

def objects():
        
    furniture = productcat(id=1,**babel_values('name',
        en="Furniture",et=u"Mööbel",de="Möbel",fr="Meubles"))
    yield furniture
    #print "foo", furniture.id, furniture
    hosting = productcat(id=2,**babel_values('name',
        en="Website Hosting",
        et=u"Veebimajutus",
        de="Website-Hosting",
        fr=u"Hébergement de sites Internet"))
    yield hosting 
    
        
    kw = babel_values('name',
          en="Wooden table",
          et=u"Laud puidust",
          de="Tisch aus Holz",
          fr=u"Table en bois")
    kw.update(babel_values('description',
          en="""\
This table is made of pure wood. 
It has **four legs**.
Designed to fit perfectly with **up to 6 wooden chairs**.
Product of the year 2008.""",
          et=u"""\
See laud on tehtud ehtsast puust.
Sellel on **neli jalga**.
Disainitud sobida kokku **kuni 6 puidust tooliga**.
Product of the year 2008.""",
          de=u"""\
Dieser Tisch ist aus echtem Holz.
Er hat **vier Beine**.
Passt perfekt zusammen mit **bis zu 6 Stühlen aus Holz**.
Produkt des Jahres 2008.""",
          fr=u"""\
Cette table est en bois authentique.
Elle a **quatre jambes**.
Conçue pour mettre jusqu'à **6 chaises en bois**.
Produit de l'année 2008.""",
          ))
    yield product("199.99",1,**kw)
    yield product("99.99",1,**babel_values('name',
        en="Wooden chair",
        et=u"Tool puidust",
        de="Stuhl aus Holz",
        fr=u"Chaise en bois"))
    yield product("129.99",1,**babel_values('name',
        en="Metal table",
        et=u"Laud metallist",
        de="Tisch aus Metall",
        fr=u"Table en métal"))
    yield product("79.99",1,**babel_values('name',
        en="Metal chair",
        et=u"Tool metallist",
        de="Stuhl aus Metall",
        fr=u"Chaise en métal"))
    hosting = product("3.99",2,
      **babel_values('name',
        en="Website hosting 1MB/month",
        et=u"Majutus 1MB/s",
        de="Stuhl aus Metall",
        fr=u"Chaise en métal"))
    yield hosting
    yield product("30.00",2,
      **babel_values('name',
        en="IKT consultation & maintenance",
        et=u"IKT konsultatsioonid & hooldustööd",
        de="IKT Konsultierung & Unterhalt",
        fr=u"Consultation & maintenance"))
    yield product("35.00",2,
      **babel_values('name',
        en="Server software installation, configuration and administration",
        et=u"Serveritarkvara installeerimine, seadistamine ja administreerimine",
        de="Server software installation, configuration and administration",
        fr=u"Server software installation, configuration and administration"))
    
    yield product("40.00",2,
      **babel_values('name',
        en="Programming",
        et=u"Programmeerimistööd",
        de="Programmierung",
        fr=u"Programmation"))
        
    yield product("25.00",2,
      **babel_values('name',
        en="Image processing and website content maintenance",
        et=u"Pilditöötlus ja kodulehtede sisuhaldustööd",
        de="Programmierung",
        fr=u"Programmation"))
    
