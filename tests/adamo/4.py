# coding: latin1
## Copyright Luc Saffre 2003-2004.

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
a very short test for when I am working in adamo...
"""
import unittest

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *


class Case(unittest.TestCase):
    "Does the default demo database startup()"

    def setUp(self):
        self.db = demo.beginSession()

    def tearDown(self):
        self.db.shutdown()


    def test01(self):
        NATIONS = self.db.query(Nations)
        self.db.setBabelLangs('en')
        self.assertEqual(NATIONS.peek('ee').name, 'Estonia')
        
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
            

if __name__ == '__main__':
    unittest.main()

