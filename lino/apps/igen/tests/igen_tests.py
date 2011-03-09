# -*- coding: utf-8 -*-
## Copyright 2011 Luc Saffre
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

import logging
logger = logging.getLogger(__name__)

#~ from django.utils import unittest
#~ from django.test.client import Client
#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
#~ from lino.modlib.contacts.models import Companies

from lino.tools import resolve_model
#Companies = resolve_model('contacts.Companies')
from lino.utils.test import TestCase

#~ Person = resolve_model('contacts.Person')
Invoice = resolve_model('sales.Invoice')
#~ Property = resolve_model('properties.Property')
#~ PersonProperty = resolve_model('properties.PersonProperty')

class DemoTest(TestCase):
    #~ fixtures = [ 'std','demo' ]
    fixtures = 'std few_countries few_languages demo_cities demo'.split()
            
def test01(self):
    """
    """
    self.assertEqual(Invoice.objects.all().count(),46)
    i = Invoice.objects.all()[0]
    self.assertEqual(unicode(i),u"Invoice # 1")
    s = i.recipient.address()
    self.assertEquals(s,u"""\
Rumma & Ko OÜ
Tartu mnt 71
10115 Tallinn
Estonia""")
