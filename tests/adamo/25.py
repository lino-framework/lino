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

import pysqlite2.dbapi2 as sqlite 


class Case(TestCase):
    
    def test01(self):
        
        self.assertEqual(sqlite.version,'2.0.3')

        conn = sqlite.connect(':memory:')
        csr = conn.cursor()
        csr.execute("""
CREATE TABLE Days (
     date INT,
  remark VARCHAR(50),
  PRIMARY KEY (date)
);
        """)
        csr.execute("""
CREATE TABLE UsageTypes (
     id CHAR(2),
  name VARCHAR(50),
  PRIMARY KEY (id)
);
        """)
        csr.execute("""
CREATE TABLE Resources (
     id VARCHAR(50),
  name VARCHAR(50),
  PRIMARY KEY (id)
);
        """)
        csr.execute("""
CREATE TABLE Usages (
     id BIGINT,
  date_date INT,
  start CHAR(8),
  stop CHAR(8),
  type_id CHAR(2),
  remark VARCHAR(50),
  resource_id VARCHAR(50),
  PRIMARY KEY (id)
);
        """)
        csr.execute("""
        CREATE TABLE Tester (
        id int,
        name varchar(80)
        )
        """)
        #conn.commit()
        for i in range(1000):
            csr.execute("""
INSERT INTO Tester VALUES (%d, 'This is row %d')
            """ % (i,i))
            #conn.commit()
            
        for i in range(732098,732126):
            csr.execute("""
INSERT INTO Days (
date, remark ) VALUES ( %d, NULL );
            """ % i)
            
        #conn.commit()
        csr.execute("""SELECT id, name from Tester
        WHERE id == 517 
        """)
        #self.assertEqual(csr.rowcount,1)
        rows = csr.fetchall()
        row=rows[0]
        self.assertEqual(row[0],517)
        
        #csr.execute("""SELECT id, name, curr from Nations
        #WHERE id = 'foo'
        #""")
        
        #conn.commit()
        conn.commit()
        
        conn.close()
        try:
            conn.commit()
            self.fail("failed to raise ProgrammingError")
        except sqlite.ProgrammingError:
            # ProgrammingError: Cannot operate on a closed database.
            pass
        
        #row = csr.fetchone()
        #rows = csr.fetchall()
        #row=rows[0]
        #self.assertEqual(row,None)
        
        

if __name__ == '__main__':
    main()

