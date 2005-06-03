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

from lino.adamo import center
from lino.adamo.database import Database
#from lino.adamo.dbds.sqlite_dbd import Connection
from lino.schemas.sprl.sprl import Sprl
from lino.schemas.sprl.tables import *
from lino.schemas.sprl import demo

sharedTables = (Languages, Nations, 
                PartnerTypes, Currencies,
                AuthorEventTypes,
                PubTypes,
                ProjectStati, Users) 

class Case(TestCase):
    todo="shared tables with different babelLangs"

    def test01(self):

        app = Sprl()
    
        app.setupSchema()
        
        app.initialize()
        
        # print app._tables
        
        conn = center.connection()
        
        stddb = app.database("std",
                             langs="en de fr et",
                             label="shared data")

        stddb.connect(conn,sharedTables)


        db = app.database(langs="de")
        db.update(stddb)
        conn = center.connection()
        db.connect(conn)
        sess1=db.startup()
        sess1.populate(demo.Populator(big=True))
        
        
        db = app.database(langs="en")
        db.update(stddb)
        conn = center.connection()
        db.connect(conn)
        sess2=db.startup()
        sess2.populate(demo.Populator(big=True))
        


        q = sess1.query(Nations,"id name area",pageLen=10,
                        search="%be%")
        self.assertEqual(q.getLangs(),"de")
        self.assertEqual(q.getDatabase().getLangs(),"en de fr et")
        q.report(width=50)
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

        

if __name__ == '__main__':
    main()

