# -*- coding: utf-8 -*-
## Copyright 2008-2010 Luc Saffre
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
This is mostly obsolete and not active.
"""

from django.test import TestCase
from django.forms.models import modelform_factory, formset_factory
from django.contrib.auth.models import User

from lino import layouts
from lino.utils.instantiator import i2d
from lino.modlib.sales import models as sales


class SalesTest: #(TestCase):
    urls = 'igen.demo.urls'
    def test01(self):
        luc = sales.Customer(firstName="Luc",lastName="Saffre")
        luc.save()
        #INV = sales.Invoice.get_journal_by_docclass()
        #~ i = INV.create_document()
        #~ i.save()
        #~ print i

class SalesTestOnDemo: #(TestCase):
    urls = 'mysites.demo.urls'
    fixtures = [ 'demo' ]
        
    def test01(self):
        luc = sales.Customer.objects.get(pk=2)
        self.assertEquals(unicode(luc), 'Luc Saffre')
        self.assertEquals(luc.as_address("\n"), u'''\
Mr. Luc Saffre
Rummajaani talu
Vana-Vigala küla
Vigala vald
78003 Raplamaa''')

    #~ def test02(self):
      
        """A simple query. Select all contacts whose lastName contains an 'a', ordered by lastName.
        """
        
        s="\n".join([unicode(c) 
          for c in sales.Customer.objects.filter(
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

        s="\n".join([
          unicode(d)+" "+str(d.creation_date)+" "+unicode(d.customer)
          for d in sales.SalesDocument.objects.all().order_by('creation_date')])
        print "\n"+s
        self.assertEquals(s,u"""\
""")

        
    #~ def test08(self):
        c = sales.Customer.objects.get(pk=4)
        s = sales.DocumentsByCustomer().as_text(master_instance=c)
        print __file__, "test08()\n"+s
        self.assertEquals(s.split(),u"""
Bäckerei Ausdemwald (Alfons Ausdemwald) : documents by customer
===============================================================
number         |creation date  |total_incl     |total excl     |total vat
---------------+---------------+---------------+---------------+---------------
2              |2009-04-12     |449.95         |449.95         |0
5              |2009-04-12     |449.95         |449.95         |0
6              |2009-04-13     |420.95         |420.95         |0        
""".split(),"DocumentsByCustomer().as_text() has changed in demo")
        
        
        
        
    #~ def test10(self):
      
        def test_context(url):
            response = self.client.get(url) # ,follow=True)
            self.failUnlessEqual(response.status_code, 200,
              "GET %r fails to respond" % url)
            return response.context
            
        context = test_context('/sales/invoices?row=1')
        self.assertEqual(context[0].get("title"),u"Sorry")
        
        User.objects.create_superuser('root','luc.saffre@gmx.net','1234')
        url = '/accounts/login/'
        response = self.client.post(url,
            dict(username='root',password='1234'))
        #~ self.failUnlessEqual(response.status_code, 200,
          #~ "POST %r failed with status %d" % (url,response.status_code))

        # now we just check whether some methods raise an exception
        # templates silently ignore them
        context = test_context('/sales/invoices/1')
        report = context[0].get("report")
        s = report.layout.as_html()
        
        context = test_context('/sales/invoices/1?editing=1')
        report = context[0].get("report")
        s = report.layout.as_html()
        
        context = test_context('/sales/invoices?editing=1')
        report = context[0].get("report")
        s = report.navigator()
        for row in report.rows():
            s = row.as_html()
            
        context = test_context('/docs/invoices?editing=0')
        report = context[0].get("report")
        s = report.navigator()
        for row in report.rows():
            s = row.as_html()
            

