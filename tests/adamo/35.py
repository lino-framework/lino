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
multiple databases and connections
"""

from lino.misc.tsttools import TestCase, main
from lino.ui import console

from lino.adamo import center
from lino.adamo.database import Database
from lino.adamo.dbds.sqlite_dbd import Connection
from lino.schemas.sprl.sprl import makeSchema
from lino.schemas.sprl.tables import *


sharedTables = (Languages, Nations, 
                PartnerTypes, Currencies,
                AuthorEventTypes,
                PubTypes,
                ProjectStati, Users) 

class Case(TestCase):


    def test01(self):

        schema = makeSchema(big=True) 
    
        schema.initialize()
        
        conn = Connection(schema=schema)
        
        stddb = schema.addDatabase(langs="en de fr et",
                                   name="std",
                                   label="shared data")

        stddb.connect(conn,sharedTables)


        db1 = schema.addDatabase(langs="de")
        db1.update(stddb)
        conn = Connection(filename="db1.db", schema=schema)
        db1.connect(conn)
        
        db2 = schema.addDatabase(langs="en")
        db2.update(stddb)
        conn = Connection(filename="db2.db", schema=schema)
        db2.connect(conn)


        sess = center.startup()
        
        sess.use(db1)
        q = sess.query(Nations,"id name area",pageLen=10,
                       search="%be%")
        self.assertEqual(q.getLangs(),"de")
        self.assertEqual(q.getDatabase().getLangs(),"en de fr et")
        sess.startDump()
        q.executeReport()
        s = sess.stopDump()
        
        self.assertEqual(s,"""\
Nations
=======
id|name                                              |area    
--+--------------------------------------------------+--------
be|Belgium                                           |30510   
bj|Benin                                             |112620  
bm|Bermuda                                           |53      
by|Belarus                                           |207600  
bz|Belize                                            |22966   
ci|Ivory Coast (Cote D'Ivoire)                       |        
lr|Liberia                                           |111370  
uz|Uzbekistan                                        |447400  
""")        

        

if __name__ == '__main__':
    main()

