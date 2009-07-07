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
from lino.django.utils.validatingmodel import TomModel, ModelValidationError
from lino.django.utils.reports import Report
from lino.django.utils.render import ViewReportRenderer
from django.db import models
from django.forms.models import modelform_factory, formset_factory
from django.conf import settings

class Contact(TomModel):
    #id_code = models.CharField(max_length=6,primary_key=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    
    def before_save(self):
        if len(self.fname) == 0:
          raise ModelValidationError("first name may not be empty")
          
class Country(TomModel):
    isocode = models.CharField(max_length=2,primary_key=True)
    name = models.CharField(max_length=200)
          

class Contacts(Report):
    columnNames = "lname fname"
    queryset=Contact.objects.order_by("lname","fname")

class Countries(Report):
    queryset=Country.objects.order_by("isocode")
    columnNames="isocode name"

    
    
    


class MenuTest(TestCase):
    def test01(self):
        c = Contact(fname="Luc",lname="Saffre")
        c.save()
        
        self.assertEqual(c.get_url_path(),"/instance/tom/Contact/1")
        
        c = Contact(lname="Saffre")
        try:
            c.save()
        except ModelValidationError,e:
            pass
        else:
            self.fail("expected ValidationError")
        
    def test03(self):
        from lino.django.utils.menus import Menu
        from lino.django.utils.models import Contacts, Persons, Products
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
<li><a href="/main/m1">Contacts</a>
<ul class="menu2">
<li><a href="/main/m1/contacts">Contacts</a></li>
<li><a href="/main/m1/persons">Persons</a></li>
</ul>
</li>
<li><a href="/main/m2">Products</a>
<ul class="menu2">
<li><a href="/main/m2/products">Products</a></li>
</ul>
</li>
</ul>
""".split())

    #~ def test04(self):
        #~ settings.MAIN_MENU

    #~ def test04(self):
        #~ rpt=Contacts()
        #~ rnd=ViewReportRenderer(rpt,"test")
        #~ response = rnd.view(self.client.request())
        #~ s=rnd.navigator()
        #~ #print "\n"+s
        #~ self.assertEquals(s.split(),u"""
        #~ """.split())
        

    def test05(self):
        form_class = modelform_factory(Contact)
        fs_class = formset_factory(form_class,can_delete=True,extra=1)
        fs = fs_class()
        s=fs.as_table()
        #print "\n"+s
        self.assertEquals(s.split(),u"""
<input type="hidden" name="form-TOTAL_FORMS" value="1" id="id_form-TOTAL_FORMS" /><input type="hidden" name="form-INITIAL_FORMS" value="0" id="id_form-INITIAL_FORMS" />
<tr><th><label for="id_form-0-fname">Fname:</label></th><td><input id="id_form-0-fname" type="text" name="form-0-fname" maxlength="20" /></td></tr>
<tr><th><label for="id_form-0-lname">Lname:</label></th><td><input id="id_form-0-lname" type="text" name="form-0-lname" maxlength="20" /></td></tr>
<tr><th><label for="id_form-0-DELETE">Delete:</label></th><td><input type="checkbox" name="form-0-DELETE" id="id_form-0-DELETE" /></td></tr>        
        """.split())
        
        
