# coding: latin1

## Copyright 2005 Luc Saffre

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

from unittest import TestCase, main

from lino.adamo.dbds.sqlite_dbd import sqlite
#import pysqlite2.dbapi2 as sqlite 


class Case(TestCase):
    
    """

    pysqlite 2.0.3 raises "OperationalError: Unable to close due to
    unfinalised statements" during commit() if one or more cursors
    have not been "used up".

    """
    
    def test01(self):

        if sqlite.version != '2.0.3': return
        conn = sqlite.connect(':memory:')
        csr = conn.cursor()
        
        # create and fill Tester table
        csr.execute("CREATE TABLE Versuch (id int, name varchar(80))")
        sql="INSERT INTO Versuch VALUES (%d, 'This is row %d')"
        for i in range(100):
            csr.execute( sql % (i,i))
            
        csr.execute("SELECT id, name from Versuch WHERE id < 10")
        # don't do anything with the cursor
        try:
            conn.close()
            self.fail("failed to raise OperationalError")
        except sqlite.OperationalError:
            pass
            # known bug in pysqlite 2.0.3
        

if __name__ == '__main__':
    main()

