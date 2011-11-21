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
multiple databases and connections with different BabelLangs

What's wrong: There are 3 calls to addDatabase() although logically
there is only 2 databases.  The shared tables must not be in a
database, but the Application must be Context. To check: will Query
and Store still work if they know only a Context, not a Database?

"""

from lino.misc.tsttools import TestCase, main
#from lino.ui import console

#from lino.adamo import center
from lino.console import syscon
from lino.adamo.database import Database
from lino.adamo.dbsession import DbContext
#from lino.adamo.dbds.sqlite_dbd import Connection
from lino.apps.contacts.contacts_tables import *
from lino.apps.contacts import contacts_demo as demo
#from lino.apps.ledger.ledger_tables import *


class Case(TestCase):
    todo="shared tables with different babelLangs"

    def test01(self):
        sharedTables = (Nation, 
                        PartnerType,
                        #Currency,
                        #User
                        ) 

        sch = ContactsSchema()
    
        conn = syscon.connection()
        
        stddb = sch.database("std",
                             langs="en de fr et",
                             label="shared data")

        stddb.connect(conn,sharedTables)


        db = sch.database(langs="de")
        db.update(stddb)
        conn = center.connection()
        db.connect(conn)
        sess1=DbContext(db)
        sess1.populate(demo.StandardPopulator(big=True))
        
        
        db = sch.database(langs="en")
        db.update(stddb)
        conn = center.connection()
        db.connect(conn)
        sess2=DbContext(db)
        sess2.populate(demo.StandardPopulator(big=True))
        


        q = sess1.query(Nation,"id name area",pageLen=10,
                        search="%be%")
        self.assertEqual(q.getLangs(),"de")
        self.assertEqual(q.getDatabase().getLangs(),"en de fr et")
        q.show(width=50)
        s = self.getConsoleOutput()
        #print s
        self.assertEqual(s,"""\
Nations
=======
id|name                                  |area    
--+--------------------------------------+--------
be|Belgium                               |30510   
bj|Benin                                 |112620  
bm|Bermuda                               |53      
by|Belarus                               |207600  
bz|Belize                                |22966   
ci|Ivory Coast (Cote D'Ivoire)           |        
lr|Liberia                               |111370  
uz|Uzbekistan                            |447400  
""")        

        
        # some other cases (for example 80.py) would fail if run
        # together with this case in one suite and if the following
        # lines were not:
        
        sess1.shutdown()
        sess2.shutdown()

if __name__ == '__main__':
    main()

