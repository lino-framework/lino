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


""" 20040206 : bug fixed

problem when accessing data that was already in the database.

In the following test, p[2] returned the same row as the previous p[1]


"""
from lino.misc.tsttools import TestCase, main
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import *

#from lino.apps.addrbook import demo #.sprl import Schema
#from lino.apps.addrbook.tables import Partner
#from lino.adamo import center

class Case(TestCase):

    def test01(self):
        "Accessing data that has not been inserted using adamo"
        sess = startup(populate=False)
        
        assert len(sess.query(Contact)) == 0, \
               "db not empty: previous test run didn't shutdown"
        
        db = sess.db
        #connection = center._center._connections[0]
        connection = db._connections[0]
        
        connection.sql_exec("""
        INSERT INTO Contacts (id,name)
               VALUES (1, "Luc");
        """)

        connection.sql_exec("""
        INSERT INTO Contacts (id,name)
               VALUES (2, "Ly");
        """)

        CONTACTS = sess.query(Contact)

        luc = CONTACTS.peek(1)
        self.assertEqual(luc.id,1)
        self.assertEqual(luc.name,"Luc")
        ly = CONTACTS.peek(2)
        self.assertEqual(ly.id,2)
        self.assertEqual(ly.name,"Ly")

        self.failIf(luc.isDirty())
        self.failIf(ly.isDirty())
        
        # some other cases (for example 80.py) would fail if run
        # together with this case in one suite and if the following
        # lines were not:
        
        sess.shutdown()

    def test02(self):
        d = {}
        id1 = (1,)
        id2 = (2,)
        s1 = "Luc"
        s2 = "Ly"
        d[id1] = s1
        d[id2] = s2
        
        self.assertEqual(d[id1],'Luc')
        self.assertEqual(d[id2],'Ly')

if __name__ == '__main__':
    main()

