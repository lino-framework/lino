# -*- coding: utf-8 -*-

## Copyright 2009 Luc Saffre.
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

from django.test import TestCase
from lino.django.tom.validatingmodel import ValidatingModel, ModelValidationError
from django.db import models
from django.forms.models import modelform_factory

class Contact(ValidatingModel):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    
    def before_save(self):
        if len(self.fname) == 0:
          raise ModelValidationError("first name may not be empty")



class TestCase(TestCase):
    def test01(self):
        c = Contact(fname="Luc",lname="Saffre")
        c.save()
        
        c = Contact(lname="Saffre")
        try:
            c.save()
        except ModelValidationError,e:
            pass
        else:
            self.fail("expected ValidationError")
        
    #~ def test02(self):
        #~ from lino.django.tom.reports import get_reports
        #~ s="\n".join(get_reports().keys())
        #~ #print "\n"+s
        #~ # this will fail if test are run for a site that 
        #~ # doesn't have lino.django.voc and lino.django.igen
        #~ self.assertEquals(s.split(),u"""
#~ Persons
#~ PaymentTerms
#~ Contacts
#~ Invoices
#~ Companies
#~ Countries
#~ UnitsPerParent
#~ ShippingModes
#~ Languages
#~ Units
#~ ItemsByInvoice
#~ Products
#~ ProductCats
#~ Entries
#~ Report
#~ Orders        
        #~ """.split())
        
    def test03(self):
        from lino.django.tom.menus import Menu
        from lino.django.igen.models import Contacts, Persons, Products
        m = Menu("main","Main menu")
        def setup_menu(menu):
            m = menu.addMenu("m1","~Contacts")
            m.addAction(Contacts())
            m.addAction(Persons())
            m = menu.addMenu("m2","~Products")
            m.addAction(Products())
        setup_menu(m)
        s=m.as_html()
        #print "\n"+s
        self.assertEquals(s.split(),u"""
<ul class="menu1">
<li><a href="/main/m1">Contacts</a>&nbsp;:
<ul class="menu2">
<li><a href="/main/m1/contacts">Contacts</a></li>
<li><a href="/main/m1/persons">Persons</a></li>
</ul>
</li>
<li><a href="/main/m2">Products</a>&nbsp;:
<ul class="menu2">
<li><a href="/main/m2/products">Products</a></li>
</ul>
</li>
</ul>
""".split())
