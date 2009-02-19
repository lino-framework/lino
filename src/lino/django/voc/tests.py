# -*- coding: utf-8 -*-

## Copyright 2008-2009 Luc Saffre.
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

from models import Contact, Product, Invoice
from django.test import TestCase


class TestCase(TestCase):
    fixtures=[ 'demo.yaml' ]
    def setUp(self):
        pass
        
    def test01(self):
        luc=Contact.objects.get(id=2)
        self.assertEquals(unicode(luc), 'Mr. Luc Saffre')
        self.assertEquals(luc.asAddress("\n"), u'''\
Mr. Luc Saffre
Rummajaani talu
Vana-Vigala küla
Vigala vald
78003 Raplamaa''')

    def test02(self):
      
        """A simple query. Select all contacts whos lastName contains an 'a', ordered by lastName.
        """
        
        s="\n".join([unicode(c) 
          for c in Contact.objects.filter(
            lastName__contains="a").order_by("lastName")])
        self.assertEquals(s,u"""\
Herrn Andreas Arens
Bäckerei Alfons Ausdemwald
Dr. Bernard Bodard
Herrn Emil Eierschal
Karl Kask
Hans Flott & Co (Frau Lisa Lahm)
Mr. Luc Saffre
Mets ja Puu OÜ (Tõnu Tamme)""")

    def test03(self):
        luc=Contact.objects.get(id=2)
        i1=Invoice(number=2000,customer=luc)
        i1.save()
        i2=Invoice(customer=luc)
        i2.save()
        self.assertEquals(i2.number,2001)
        
    def test04(self):
        luc=Contact.objects.get(id=2)
        table=Product.objects.get(id=1)
        chair=Product.objects.get(id=2)
        i=Invoice(customer=luc)
        i.save()
        i.items.create(pos=1,product=table,qty=1)
        
## Run these tests using "python manage.py test".
## see http://docs.djangoproject.com/en/dev/topics/testing/#topics-testing
