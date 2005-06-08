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


"""

- new trigger validate_xx()
- "row is not locked"

"""

from lino.misc.tsttools import TestCase, main
from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *
from lino.adamo.exceptions import DataVeto, InvalidRequestError

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        
        self.sess = demo.startup()

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        NATIONS = self.sess.query(Nations)
        try:
            NATIONS.appendRow(id="foo",name="Fooland")
            self.fail("expected DataVeto")
        except DataVeto,e:
            self.assertEqual(str(e),"'foo': Nation.id must be 2 chars")


        be = NATIONS.peek('be')
        try:
            be.name = "België"
            self.fail("expected DataVeto")
        except InvalidRequestError,e:
            self.assertEqual(str(e),"row is not locked")
        
            

if __name__ == '__main__':
    main()
