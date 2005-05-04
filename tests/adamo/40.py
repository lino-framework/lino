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

adamo.filters: first use of SQL nested SELECT

List of Nations who have at least one city [whose name contains "eup"].

SELECT id, name_en
  FROM Nations
  WHERE EXISTS (
    SELECT *
        FROM Cities
        WHERE Cities.nation_id=Nations.id
            [and Cities.name like '%eup%']
    )

'''

class Case(TestCase):
    skip=True
    def setUp(self):
        TestCase.setUp(self)
        self.sess = demo.beginSession(self.ui,big=True)
        
    def tearDown(self):
        self.sess.shutdown()
        
    def test01(self):
        ds=self.sess.query(Nations,"id name")
        ds.addColumn("cities",search="eup")
        ds.addFilter(NotEmpty,"cities")
        rpt=DataReport(ds,pageLen=5,pageNum=1,columnWidths="2 15 20")
        self.ui.report(rpt)
        s=self.getConsoleOutput()
        #print __file__,"\n", s
        self.assertEquivalent(s,"""\
Nations where 'cities' not empty
================================
id|name           |cities
--+---------------+--------------------
be|Belgium        |2846 Cities
de|Germany        |7 Cities
ee|Estonia        |10 Cities
""")
        sql=ds.getSqlSelect()
        #print __file__,"\n", sql
        self.assertEquivalent(sql,"""\
SELECT id, name_en
FROM Nations
WHERE EXISTS (SELECT *
              FROM Cities
              WHERE Nations.id=Cities.nation_id)
        """)
        
if __name__ == '__main__':
    main()

