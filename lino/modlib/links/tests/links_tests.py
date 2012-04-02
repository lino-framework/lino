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

"""
This module contains "quick" tests that are run on a demo database 
without any fixture. You can run only these tests by issuing::

  python manage.py test links.QuickTest

  
"""
import logging
logger = logging.getLogger(__name__)

#~ from django.utils import unittest
#~ from django.test.client import Client
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
#~ from lino.modlib.contacts.models import Companies


from lino.utils import i2d
from lino.utils import babel
from lino.tools import resolve_model
from lino.tools import obj2str
#Companies = resolve_model('contacts.Companies')
from lino.utils.test import TestCase

from lino.modlib.links.models import Link, LinkType


class QuickTest(TestCase):
    pass
            
  
def test01(self):
    """
    Used on :doc:`/blog/2011/0414`.
    See the source code at :srcref:`/lino/apps/pcsw/tests/pcsw_tests.py`.
    """

    Person = resolve_model(settings.LINO.person_model)
    Company = resolve_model(settings.LINO.company_model)
    
    p1 = Person(first_name="First",last_name="Person")
    p1.save()
    p2 = Person(first_name="Second",last_name="Person")
    p2.save()
    c1 = Company(name="First Company")
    c1.save()
    
    lt = LinkType(name="Director",
        a_type=ContentType.objects.get_for_model(Company),
        b_type=ContentType.objects.get_for_model(Person))
    lt.save()
    
    link = Link(type=lt,a=c1,b=p1)
    link.save()
    
    p1s = unicode(p1)
    c1s = unicode(c1)
    
    self.assertEqual(unicode(link),
        "%s is Director of %s" % (p1s,c1s))
    
    self.assertEqual(link.a,c1)
    self.assertEqual(link.b,p1)
    
    link.b = p2
    link.save()
    self.assertEqual(link.b,p2)
    
    link = Link.objects.get(pk=1)
    
    self.assertEqual(link.b,p2)
    self.assertEqual(link.a,c1)
    
    try:
        link.a = p1
    except ValueError,e:
        self.assertEqual(str(e),
            "Expected <class 'lino.apps.pcsw.models.Company'> instance but got <Person: First PERSON (100)>")
    else:
        self.fail("Failed to raise ValueError")
    
    
    
