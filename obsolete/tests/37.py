# coding: latin1
## Copyright 2003-2005 Luc Saffre

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

from lino.misc.tsttools import TestCase, main
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import *

#from lino.apps.addrbook import demo
#from lino.apps.addrbook.tables import *


class Case(TestCase):
    "do the German country names get installed with big=True?"
    
    #todo="Crash in big addrbook demo"
    
    def setUp(self):
        TestCase.setUp(self)
        self.sess = startup(langs="en de", big=True)

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        NATIONS = self.sess.query(Nation)
        
        n = NATIONS.peek('al')
        self.assertEqual(n.name, 'Albania')
        self.assertEqual(n.area, 28748)
        self.sess.setBabelLangs('de')
        self.assertEqual(n.name, 'Albanien')
        
        n = NATIONS.peek('ee')
        self.sess.setBabelLangs('de')
        self.assertEqual(n.name, 'Estland')
        self.sess.setBabelLangs('en')
        self.assertEqual(n.name, 'Estonia')
        

if __name__ == '__main__':
    main()

