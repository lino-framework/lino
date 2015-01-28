# -*- coding: utf-8 -*-
# Copyright 2011 Luc Saffre
# License: BSD (see file COPYING for details)

import logging
logger = logging.getLogger(__name__)

#~ from django.utils import unittest
#~ from django.test.client import Client
#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
#~ from lino.modlib.contacts.models import Companies

from lino.core.utils import resolve_model
#Companies = resolve_model('contacts.Companies')
from lino.utils.djangotest import TestCase

#~ Person = resolve_model('contacts.Person')
Invoice = resolve_model('sales.Invoice')
#~ Property = resolve_model('properties.Property')
#~ PersonProperty = resolve_model('properties.PersonProperty')


class DemoTest(TestCase):
    #~ fixtures = [ 'std','demo' ]
    fixtures = 'std few_countries few_languages few_cities demo'.split()


def test01(self):
    """
    """
    self.assertEqual(Invoice.objects.all().count(), 28)
    i = Invoice.objects.all()[0]
    self.assertEqual(unicode(i), u"Invoice # 1")
    s = i.customer.address()
    self.assertEquals(s, u"""\
Rumma & Ko OÜ
Tartu mnt 71
10115 Tallinn
Estonia""")
