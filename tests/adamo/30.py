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


"""

- testing ConsoleSession.report()

"""

from lino.misc.tsttools import main, TestCase

from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import *
from lino.adamo import DataVeto, InvalidRequestError
from lino.reports import DataReport

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.sess = demo.startup(self.ui)

    def tearDown(self):
        self.sess.shutdown()


    def test01(self):
        "report with a Pointer"
        ds =self.sess.query(Cities,"id name nation",
                           orderBy="name",
                           pageLen=10)
                           
        # print [col.name for col in rpt._clist.visibleColumns]
        #self.sess.startDump()
        #q.executeReport(columnWidths="5 50 10")
        rpt=DataReport(ds,columnWidths="5 50 10")
        self.ui.report(rpt)

        s = self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""\
Cities
======
id   |name                                              |nation    
-----+--------------------------------------------------+----------
1    |Aachen                                            |Germany   
7    |Alfter-Oedekoven                                  |Germany   
3    |Berlin                                            |Germany   
4    |Bonn                                              |Germany   
2    |Brugge                                            |Belgium   
1    |Bruxelles                                         |Belgium   
9    |Charleroi                                         |Belgium   
6    |Eschweiler                                        |Germany   
3    |Eupen                                             |Belgium   
5    |Kelmis                                            |Belgium   
""")
        
    def test02(self):
        "report with a BabelField"
        ds = self.sess.query(Nations,"id name")
        #self.sess.startDump()
        rpt=DataReport(ds,columnWidths="2 25")
        self.ui.report(rpt)
        #q.executeReport(columnWidths="2 25")
        s = self.getConsoleOutput()
        # print s
        self.assertEquivalent(s,"""\
Nations
=======
id|name                     
--+-------------------------
ee|Estonia                  
be|Belgium                  
de|Germany                  
fr|France                   
us|United States of America 
""")

if __name__ == '__main__':
    main()
