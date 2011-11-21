# coding: latin1

## Copyright 2005-2007 Luc Saffre

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

from lino.adamo.dbds.sqlite_dbd import sqlite
#import pysqlite2.dbapi2 as sqlite

from unittest import TestCase, main

class Case(TestCase):

    """Basic concurrency experiments in sqlite after reading
    http://sqlite.org/lockingv3.html """
    
    def test01(self):

        conn = sqlite.connect(':memory:')
        csr1 = conn.cursor()

        csr1.execute("""CREATE TABLE Partners (
        id BIGINT,
        name VARCHAR(50),
        PRIMARY KEY (id)
        );""")
        
        csr1.execute("""INSERT INTO Partners (id, name)
        VALUES ( 1, 'Anton Ausdemwald')""")

        csr1.execute("""INSERT INTO Partners (id, name)
        VALUES ( 2, 'Andreas Arens')""")

        csr1.execute("""SELECT id, name FROM Partners;""")

        # Executing a SELECT causes a shared lock to be placed on the
        # queried table(s) until the cursor's result has been
        # completely retrieved.  That's why an UPDATE (or INSERT or
        # DELETE) in this table using *another* cursor will be
        # refused:
        
        csr2 = conn.cursor()
        try:
            csr2.execute("""
            UPDATE Partners SET name = 'Arens, Andreas'
            WHERE id = 2; """)
            self.fail("failed to raise OperationalError")
        except sqlite.OperationalError,e:
            self.assertEqual(
                str(e),\
                "database table is locked")

        # As soon as csr1 has finished to retrieve its result (for
        # example by doing fetchall()) the table lock is released and
        # we can run the UPDATE using csr2:

        s=str(csr1.fetchall())
        #print s
        self.assertEqual(
            s,"[(1, u'Anton Ausdemwald'), (2, u'Andreas Arens')]")
        
        csr2.execute("""
        UPDATE Partners SET name = 'Arens, Andreas'
        WHERE id = 2; """)

##         20070105 The following seems no longer to raise OperationalError
        
##         # trying to close your connection while there is at least one
##         # open cursor will raise an exception:

##         try:
##             conn.close()
##             self.fail("failed to raise OperationalError")
##         except sqlite.OperationalError,e:
##             self.assertEqual(
##                 str(e),\
##                 "Unable to close due to unfinalised statements")

        # closing a cursor is done either by deleting its reference or
        # alternatively by calling close() explicitly

        del csr1, csr2
        
        conn.close()
        

if __name__ == '__main__':
    main()





