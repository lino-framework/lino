#coding: latin1
## Copyright 2003-2007 Luc Saffre

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

from lino.adamo.store import Populator

#from lino.apps.timings.timings_tables import Timings
     
from lino.apps.timings import timings_tables as tables
from lino.adamo.datatypes import itot
#from lino.adamo import center

class TestPopulator(Populator):
    def populateUsageTypes(self,q):
        self.a=q.appendRow(id="A",name="Arbeit")
        self.u=q.appendRow(id="U",name="Urlaub")
        self.m=q.appendRow(id="M",name="Mission")
        self.k=q.appendRow(id="K",name="Krank")
        self.types=(self.a,self.u,self.m,self.k)

    def populateResources(self,q):
        self.luc=q.appendRow(id="luc",name="Luc")
        self.gerd=q.appendRow(id="gerd",name="Gerd")
        
    def populateDays(self,q):
        for d in tables.everyday(20050601,20050731):
            q.appendRow(date=d)

    def populateUsages(self,q):
        days=q.getContext().query(tables.Day)
        for d in tables.everyday(20050620,20050624):
            q.appendRow(resource=self.luc,
                        date=days.peek(d),
                        start=itot(530),
                        stop=itot(2145),
                        type=self.a)
        for d in tables.everyday(20050625,20050628):
            q.appendRow(resource=self.luc,
                        date=days.peek(d),
                        type=self.k)
            
        for d in tables.everyday(20050628,20050702):
            q.appendRow(resource=self.gerd,
                        date=days.peek(d),
                        type=self.k)


class Case(TestCase):
    verbosity=0
    todo="Timings needs gendoc.html_site which is broken"
    def setUp(self):
        TestCase.setUp(self)
        app=tables.Timings()
        #self.dbc=app.quickStartup(toolkit=Toolkit()) #,dump=True)
        self.dbc=app.createContext() # dump=True)
        app.runtask(TestPopulator(),self.dbc)

    def tearDown(self):
        self.dbc.shutdown()

    def test01(self):
        #center.startDump()
        #s=center.stopDump()
        #print s
        #self.assertEquivalent(s,""" """)        
        tables.MonthlyCalendar(self.dbc,2005,6).show()
        #self.dbc.db.app.showMonthlyCalendar(self.dbc,2005,6)
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""\
Days where 'date' == 2005-6-None
================================
date        |ISO       |Gerd                       |Luc
------------+----------+---------------------------+---------------------------
[2005-06-01]|2005-06-01|                           |
[2005-06-02]|2005-06-02|                           |
[2005-06-03]|2005-06-03|                           |
[2005-06-04]|2005-06-04|                           |
[2005-06-05]|2005-06-05|                           |
[2005-06-06]|2005-06-06|                           |
[2005-06-07]|2005-06-07|                           |
[2005-06-08]|2005-06-08|                           |
[2005-06-09]|2005-06-09|                           |
[2005-06-10]|2005-06-10|                           |
[2005-06-11]|2005-06-11|                           |
[2005-06-12]|2005-06-12|                           |
[2005-06-13]|2005-06-13|                           |
[2005-06-14]|2005-06-14|                           |
[2005-06-15]|2005-06-15|                           |
[2005-06-16]|2005-06-16|                           |
[2005-06-17]|2005-06-17|                           |
[2005-06-18]|2005-06-18|                           |
[2005-06-19]|2005-06-19|                           |
[2005-06-20]|2005-06-20|                           |A   05:30:00-21:45:00
[2005-06-21]|2005-06-21|                           |A   05:30:00-21:45:00
[2005-06-22]|2005-06-22|                           |A   05:30:00-21:45:00
[2005-06-23]|2005-06-23|                           |A   05:30:00-21:45:00
[2005-06-24]|2005-06-24|                           |A   05:30:00-21:45:00
[2005-06-25]|2005-06-25|                           |K
[2005-06-26]|2005-06-26|                           |K
[2005-06-27]|2005-06-27|                           |K
[2005-06-28]|2005-06-28|K                          |K
[2005-06-29]|2005-06-29|K                          |
[2005-06-30]|2005-06-30|K                          |
""")
        
    def test02(self):
        if True: return
        files=self.dbc.db.app._writeStaticSite(
            self.dbc,r"c:\temp\timings")
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"")
        self.assertEqual(len(files),94)
        #print sess.db._connections[0].stopDump()
        #print files



if __name__ == '__main__':
    main()

