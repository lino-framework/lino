## Copyright Luc Saffre 2003-2005

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

import types
import unittest

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

class Case(unittest.TestCase):


    def test01(self):

        schema = makeSchema(big=True) 
    
        schema.startup()
        
        conn = Connection(schema=schema)
        stddb = Database(langs="en de fr et",
                         schema=schema,
                         name="std",
                         label="shared standard data")

        stddb.connect(conn,sharedTables)


        db1 = Database( langs="de", schema=schema, name="db1")
        db1.update(stddb)
        conn = Connection(filename="db1.db", schema=schema)
        db1.connect(conn)
        
        db2 = Database( langs="en", schema=schema, name="db1")
        db2.update(stddb)
        conn = Connection(filename="db2.db", schema=schema)
        db2.connect(conn)


        sess = center.startup()
        sess.use(db1)
        q = sess.query(Nations,"id name area")
        q.report()
        #sess.query(Nations,"id name area",orderBy="area").report()

        

if __name__ == '__main__':
    unittest.main()

