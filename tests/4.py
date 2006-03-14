## Copyright 2003-2006 Luc Saffre

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

"Does the contacts demo database startup()"

from lino.misc.tsttools import TestCase, main

from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import *
#from lino.apps.addrbook import demo
#from lino.apps.addrbook import *


class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.sess = startup()

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        NATIONS = self.sess.query(Nation)
        n = NATIONS.peek('ee')
        self.assertEqual(n.name, 'Estonia')
        
        try:
            NATIONS.peek(['ee'])
        except TypeError,e:
            pass
        else:
            self.fail('Failed to raise TypeError')
            
        try:
            NATIONS.peek(1)
        except TypeError,e:
            pass
        else:
            self.fail('Failed to raise TypeError')
            

    def test02(self):
        self.sess.setBabelLangs("en")
        PARTNERS = self.sess.query(Partner)
        CITIES = self.sess.query(City)
        row = PARTNERS.peek(1)

        # print "foobar " + repr(row.getValues())

        """ The row returned by peek() is an object whose properties can
        be accessed (or not) according to the specific rules.    """

        # simple fields :
        
        ae = self.assertEqual
        
        ae(row.id,1)
        ae(row.name,"Saffre")
        ae(str(row),"Luc Saffre")

        tallinn = CITIES.findone(name="Tallinn")
        
        ae(row.city,tallinn)
        
        ae(row.city.name,"Tallinn")
        ae(row.nation.name,"Estonia")
        


    def test05(self):
        
        """ If you are going to create several rows and don't want to
        specify the field names each time, then you can create a Query:
        """

        PARTNERS = self.sess.query(Partner)
        CITIES = self.sess.query(City)
        
        q = PARTNERS.query('id firstName name')
        
        row = q.appendRow(1000,"Jean","Dupont")
        self.assertEqual(row.id,1000)
        self.assertEqual(row.firstName,"Jean")
        self.assertEqual(row.name,"Dupont")
        
        q.appendRow(1001,"Joseph","Dupont")
        q.appendRow(1002,"Juliette","Dupont")
        

    def test06(self):
        "Samples"
        
        """ If you tell a Query of Cities that you want only cities in
        Belgium, then use this query to create a city row, then this row
        will automatically know that it's nation is Belgium.    """

        NATIONS = self.sess.query(Nation)
        PARTNERS = self.sess.query(Partner)
        CITIES = self.sess.query(City)
        
        be = NATIONS.peek("be")
        q = CITIES.query(nation=be)
        q = be.cities() #.query('id name')
        stv = q.appendRow(name='Sankt-Vith')
        # print row.getValues()
        self.assertEqual(stv.nation,be)
        self.assertEqual(stv.name,"Sankt-Vith")
        # q.appendRow(21,'Eynatten')
        

if __name__ == '__main__':
    main()

