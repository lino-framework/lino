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

import datetime

from lino.adamo.dbds.sqlite_dbd import sqlite
#import pysqlite2.dbapi2 as sqlite 


class Case(TestCase):
    
    def test01(self):
        
        def month(s):
            d=datetime.date.fromordinal(s)
            return d.month
        def year(s):
            d=datetime.date.fromordinal(s)
            return d.year
        def day(s):
            d=datetime.date.fromordinal(s)
            return d.day
        
        conn = sqlite.connect( ':memory:')
        #detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
        conn.create_function("month",1,month)
        conn.create_function("year",1,year)
        conn.create_function("day",1,day)
        
        csr = conn.cursor()
        
        # create and fill Tester table
        csr.execute("CREATE TABLE Days (date date)")
        sql="INSERT INTO Days (date) VALUES ( %d )"
        for i in range(732098,732103):
            csr.execute(sql % i)
        
        csr.execute("SELECT date from Days")
        s=" ".join([str(l[0]) for l in csr.fetchall()])
        #print s
        self.assertEqual(s,"732098 732099 732100 732101 732102")
        
        csr.execute("SELECT date from Days WHERE month(date) = 6")
        s=" ".join([str(l[0]) for l in csr.fetchall()])
        #print s
        self.assertEqual(s,"732098 732099 732100 732101 732102")
        
        # don't do anything with the cursor
        try:
            conn.close()
        except sqlite.OperationalError:
            # known bug in pysqlite 2.0.3
            self.assertEqual(sqlite.version,'2.0.3')
        

if __name__ == '__main__':
    main()

