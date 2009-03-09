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

#from lino.django.tom import models
from django import forms
from django.test import TestCase

class ContactForm(forms.Form):
    id = forms.IntegerField(readonly=True)
    fname = forms.CharField(max_length=20)
    lname = forms.CharField(max_length=20)
    

from django.db import models
from django.forms.models import modelform_factory

class Contact(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)



class TestCase(TestCase):
    def test01(self):
        frm = ContactForm()
        s=frm.as_p()
        print "\n"+s
        self.assertEqual(s.split(),"""
<p><label for="id_id">Id:</label> <input readonly type="text" name="id" id="id_id" /></p>
<p><label for="id_fname">Fname:</label> <input id="id_fname" type="text" name="fname" maxlength="20" /></p>
<p><label for="id_lname">Lname:</label> <input id="id_lname" type="text" name="lname" maxlength="20" /></p>        
        """.split())
        
    def test02(self):
        contact = Contact(fname="Luc",lname="Saffre")
        contact.save()
        
        fc = modelform_factory(Contact,fields="fname lname".split())
        frm=fc(instance=contact)
        s=frm.as_p()
        #print "\n"+s
        self.assertEqual(s.split(),"""
<p><label for="id_fname">Fname:</label> <input id="id_fname" type="text" name="fname" value="Luc" maxlength="20" /></p>
<p><label for="id_lname">Lname:</label> <input id="id_lname" type="text" name="lname" value="Saffre" maxlength="20" /></p>
        """.split())
        
        fc = modelform_factory(Contact,fields="fname lname".split())
        frm=fc(instance=contact)
        s=frm.as_p()
        #print "\n"+s
        self.assertEqual(s.split(),"""
<p><label for="id_fname">Fname:</label> 
<input id="id_fname" type="text" 
  name="fname" value="Luc" maxlength="20" readonly /></p>
<p><label for="id_lname">Lname:</label> <input id="id_lname" type="text" name="lname" value="Saffre" maxlength="20"  readonly /></p>
        """.split())
        