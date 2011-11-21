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

from lino.adamo.dbds.sqlite_dbd import sqlite
#import pysqlite2.dbapi2 as sqlite

from unittest import TestCase, main

class Case(TestCase):
    
    def test01(self):

        #self.assertEqual(sqlite.version,'2.0.3')

        conn = sqlite.connect(':memory:')
        csr = conn.cursor()

        csr.execute("""CREATE TABLE Partners (
        id BIGINT,
        name VARCHAR(50),
        PRIMARY KEY (id)
        );""")
        
        #conn.commit()
        
        csr.execute("""INSERT INTO Partners (id, name)
        VALUES ( 2, 'Andreas Arens')""")

        #conn.commit()
        
##         csr.execute("""SELECT id, name FROM Partners;""")
##         self.assertEqual(len(csr.fetchall()),1)

        csr.execute("""
        UPDATE Partners SET name = 'Arens, Andreas'
        WHERE id = 2; """)
        
        csr.close()
        
        conn.commit()

        conn.close()
        

if __name__ == '__main__':
    main()





