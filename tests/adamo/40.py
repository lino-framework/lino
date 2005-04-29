# coding: latin1
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

from lino.misc.tsttools import TestCase, main
from lino.reports import DataReport
from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Nations, Cities

from lino.adamo.filters import NotEmpty

'''
subqueries.
nested search.
List of Nations who have at least one city whose name contains "eup".

SELECT id, name
  from Nations
  where any (select name, nation_id
             from Cities
             where nation_id = Nations.id and Cities.name like '%eup%')

'''

class Case(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.sess = demo.beginSession(self.ui,big=True)
        
    def tearDown(self):
        self.sess.shutdown()
        
    def test01(self):
        ds=self.sess.query(Nations,"id name cities")
        #ds.cities.configure(search="eup")
        #ds.addFilter(None,"ANY","cities")
##         def flt(row):
##             row._ds.startDump()
##             l = len(row.cities)
##             s=row._ds.stopDump()
##             print s
##             return l > 0
##         ds.addFilter(flt)
        #ds.addFilter(lambda row: len(row.cities)>0)
        ds.addFilter(NotEmpty,"cities")
        #for row in ds:
        #    print row
        rpt=DataReport(ds,pageLen=5,pageNum=1)
        self.ui.report(rpt)
        s=self.getConsoleOutput()
        print __file__
        print s
        
if __name__ == '__main__':
    main()

