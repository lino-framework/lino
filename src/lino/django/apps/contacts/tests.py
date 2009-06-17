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

from django.test import TestCase
#from lino.django.igen import models
from lino.django.apps.contacts.models import Contact, Companies
from lino.django.apps.countries.models import Country

from django.forms.models import modelform_factory, formset_factory
from lino.django.utils import layouts

class DemoTest(TestCase):
    urls = 'mysites.demo.urls'
    fixtures = [ 'demo' ]
        
    def test01(self):
        self.assertEquals(Contact.objects.count(), 16)
        luc = Contact.objects.get(id=2)
        print repr(luc)
        self.assertEquals(unicode(luc), 'Luc Saffre')
        self.assertEquals(luc.as_address("\n"), u'''\
Mr. Luc Saffre
Rummajaani talu
Vana-Vigala küla
Vigala vald
78003 Raplamaa''')

    def test02(self):
        """A simple query. Select all contacts whose lastName contains an 'a', ordered by lastName.
        """
        
        s="\n".join([unicode(c) 
          for c in Contact.objects.filter(
            lastName__contains="a").order_by("lastName")])
        #print "\n"+s
        self.assertEquals(s,u"""\
Andreas Arens
Bäckerei Ausdemwald (Alfons Ausdemwald)
Bernard Bodard
Emil Eierschal
Jérôme Jeanémart
Karl Kask
Hans Flott & Co (Lisa Lahm)
Luc Saffre
Mets ja Puu OÜ (Tõnu Tamme)""")

    def test05(self):
        s = Companies().as_text(
          column_widths=dict(companyName=20,country=12))
        #print "\n"+s
        self.assertEquals(s.split(),u"""
Companies
=========
companyName         |country     |title         |firstName     |lastName
--------------------+------------+--------------+--------------+--------------
Bernd Brecht        |Germany     |Herr          |Bernd         |Brecht
Bäckerei Ausdemwald |Belgium     |Herrn         |Alfons        |Ausdemwald
Donderweer bv       |Netherlands |              |              |
Hans Flott & Co     |Germany     |Frau          |Lisa          |Lahm
Mets ja Puu OÜ      |Estonia     |              |Tõnu          |Tamme
Minu Firma OÜ       |Estonia     |              |              |
""".split(),"Companies().as_text() has changed in demo")
        
        
        
    def test10(self):
        for url in (
          '',
          '/contacts',
          '/contacts/contacts',
          '/contacts/contacts?editing=1',
          '/contacts/contacts?editing=0',
          #'/instance/igen/Contact/1',
        ):
            response = self.client.get(url) # ,follow=True)
            self.failUnlessEqual(response.status_code, 200,
              "GET %r fails to respond" % url)

        # now we just check whether some methods raise an exception
        # templates silently ignore them
        response = self.client.get('/contacts/contacts')
        s = "\n".join([repr(c) for c in response.context])
        renderer = response.context[0].get("report")
        s = renderer.navigator()
        count = 0
        for row in renderer.rows():
            s = row.as_html()
            count += 1
        self.assertEqual(count,15)
        
        response = self.client.get('/config/languages/1')
        report = response.context[0].get("report")
        s = report.layout.as_html()

        response = self.client.get('/contacts/contacts/1?editing=1')
        report = response.context[0].get("report")
        s = report.layout.as_html()
        s = report.navigator()
        
