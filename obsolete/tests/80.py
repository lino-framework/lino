## Copyright 2006 Luc Saffre

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
#from lino.apps.addrbook.tables import City
#from lino.adamo import center

class Case(TestCase):
    def test01(self):
        sess = startup()
        sess.startDump()

        # method 1 needs
        qry=sess.query(City)
        home=qry.findone(name="Eupen")
        
        sql=sess.peekDump()
        #print sql
        self.assertEquivalent(sql,"""\
        SELECT nation_id, id, name, zipCode, inhabitants
        FROM Cities
        WHERE name = 'Eupen';
        """)
        
        self.assertEqual(home.nation.name,"Belgium")
        sql=sess.peekDump()
        self.assertEquivalent(sql,"""\
        SELECT id, name_en, area, population, curr, isocode
        FROM Nations
        WHERE id = 'be';
        """)
        
        qry=sess.query(City,"id name nation.name")
        home=qry.findone(name="Eupen")
        sql=sess.peekDump()
        #print sql
        self.assertEquivalent(sql,"""
        SELECT lead.nation_id, lead.id, lead.name,
               nation.id, nation.name_en
        FROM Cities AS lead
          LEFT JOIN Nations AS nation ON (lead.nation_id = nation.id)
        WHERE name = 'Eupen';
        """)
        
        self.assertEqual(home.nation.name,"Belgium")
        sql=sess.peekDump()
        self.assertEquivalent(sql,"")
        
        # some other cases (for example 80.py) would fail if run
        # together with this case in one suite and if the following
        # lines were not:
        
        sess.shutdown()
    
if __name__ == '__main__':
    main()
