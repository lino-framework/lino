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

import os
import codecs
import pysqlite2.dbapi2 as sqlite

from unittest import TestCase, main


filename=os.path.join(os.path.dirname(__file__),"27b.sql")

class Case(TestCase):
    
    def test01(self):

        conn = sqlite.connect(':memory:')
        csr = conn.cursor()
        
        f=codecs.open(filename,encoding="cp1252")
        sql=""
        lengths=[]
        inserts=0
        for ln in f:
            ln=ln.strip()
            if not ln.startswith('#'):
                if ln.endswith(";"):
                    sql += ln[:-1]
                    csr.execute(sql)
                    #conn.commit()
                    
                    #print sql
                    #print
                    
                    if sql.startswith("SELECT "):
                        # use the cursor up to avoid work around
                        # pysqlite bug
                        
                        #for t in csr:
                        #    print t
                        lengths.append(len(csr.fetchall()))
                        
                        #print "--> %d rows" % len(csr.fetchall())
                    elif sql.startswith("INSERT "):
                        inserts+=1
                    csr.close()
                    
                    #else:
                    #    conn.commit()
                    #    print "(conn.commit())"
                    sql=""
                else:
                    sql+=ln
                
        conn.close()
        #print lengths
        #print "%d INSERT statements" % inserts
        
##         self.assertEqual(lengths,
##                          [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
##                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
##                          0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 7])

        self.assertEqual(
            lengths,
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
             1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 15, 1, 5]
            )
                         
        self.assertEqual(inserts,5191)
        

if __name__ == '__main__':
    main()





