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


from django.test import TestCase
#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
from lino.modlib.contacts.models import Companies

from lino.modlib.tools import resolve_model
Person = resolve_model('contacts.Person')
#Companies = resolve_model('contacts.Companies')

class DemoTest(TestCase):
    fixtures = [ 'demo' ]
        
    def test01(self):
        self.assertEquals(Person.objects.count(), 16)
        luc = Person.objects.get(id=2)
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
        
        s = "\n".join([unicode(c) 
          for c in Person.objects.filter(
            lastName__contains="a").order_by("lastName")])
        #print "\n"+s
        self.assertEquals(s,u"""\
Andreas Arens
Bernard Bodard
Emil Eierschal
Jérôme Jeanémart
Karl Kask
Luc Saffre""")

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
        
        
        
