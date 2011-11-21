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
20050111 : I submitted a bug report to pysqlite:
http://sourceforge.net/tracker/index.php?func=detail&aid=1100047&group_id=54058&atid=472543

sqlite.__revision__ = '1.22'
sqlite.apilevel = '2.0'
sqlite.threadsafety = 1
sqlite.version = '1.1.6'
sqlite.version_info = (1, 1, 6)

Cursor.rowcount is 1 although it should be 0 after a
SELECT that returns no rows. Here is a testcase to
demonstrate this bug::


"""


from types import TupleType
from unittest import TestCase, main

from lino.adamo.dbds.sqlite_dbd import sqlite
## if True:
##     import pysqlite2.dbapi2 as sqlite # pysqlite 2.0
## else:
##     import sqlite


class Case(TestCase):


    def test01(self):

        conn = sqlite.connect(':memory:')
        #csr = sqlite.Cursor(conn,TupleType)
        csr = conn.cursor()
        csr.execute("""CREATE TABLE Nations (
        id char(50),
        name varchar(80),
        curr char(3))
        """)
        csr.execute("""INSERT INTO Nations VALUES
        ('be', 'Belgium', 'EUR')
        """)
        csr.execute("""INSERT INTO Nations VALUES
        ('ee', 'Estonia', 'EEK')
        """)
        
        csr.execute("""SELECT id, name, curr from Nations
        WHERE id = 'ee'
        """)
        #self.assertEqual(csr.rowcount,1)
        row = csr.fetchone()
        self.assertEqual(row[0],'ee')
        self.assertEqual(row[1],'Estonia')
        self.assertEqual(row[2],'EEK')
        
        csr.execute("""SELECT id, name, curr from Nations
        WHERE id = 'foo'
        """)
        
        # this fails with pysqlite
        #self.assertEqual(csr.rowcount,0)
        row = csr.fetchone()
        self.assertEqual(row,None)
        



if __name__ == '__main__':
    main()

