#coding: latin1
## Copyright 2003-2005 Luc Saffre

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
   
from lino.misc.tsttools import TestCase, main, Toolkit

from lino.adamo.store import Populator

from lino.apps.timings.timings import Timings
from lino.apps.timings.tables import *
from lino.adamo.datatypes import itod

class TestPopulator(Populator):
    def populateUsageTypes(self,q):
        self.a=q.appendRow(id="A ",name="Arbeit")
        self.u=q.appendRow(id="U ",name="Urlaub")
        self.m=q.appendRow(id="M ",name="Mission")

    def populateResources(self,q):
        self.ls=q.appendRow(id="luc",name="Luc")
        self.gx=q.appendRow(id="gerd",name="Gerd")
        
    def populateDays(self,q):
        for i in range(20050601,20050630):
            q.appendRow(date=itod(i))

    def populateUsages(self,q):
        days=q.getSession().query(Days)
        for i in range(20050601,20050630):
            d=days.peek(itod(i))
            q.appendRow(resource=self.ls,
                        date=d,
                        type=self.a)


class Case(TestCase):
    
    def test01(self):
        app=Timings()
        sess=app.quickStartup(toolkit=Toolkit()) #,dump=True)
        sess.populate(TestPopulator())
        #sess.commit()
        
        #app.showMainForm(sess)
        #s=self.getConsoleOutput()
        #print s
        
        files=app._writeStaticSite(sess,r"c:\temp\timings")
        s=self.getConsoleOutput()
        print s
        self.assertEquivalent(s,"")
        self.assertEqual(len(files),58)
        #print sess.db._connections[0].stopDump()
        sess.commit()
        #print files



if __name__ == '__main__':
    main()

