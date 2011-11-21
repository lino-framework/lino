# coding: iso-8859-1

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
from lino.apps.pizzeria import services
from lino.apps.pizzeria.pizzeria import Customer


class Case(TestCase):
    """
    (this failed on 20040322)
    """

    def setUp(self):
        TestCase.setUp(self)
        app=services.MyPizzeria()
        self.sess=app.createContext()
        services.populate(self.sess)

    def tearDown(self):
        self.sess.shutdown()

    def test01(self):
        CUST = self.sess.query(Customer)
        c = CUST.appendRow(name="Mark")
        newID = c.id
        c = CUST.peek(newID)
        self.assertEqual(c.id,newID) # failed
        
if __name__ == '__main__':
    main()

