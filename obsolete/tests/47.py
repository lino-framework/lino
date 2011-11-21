## Copyright 2005-2006 Luc Saffre

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
#from lino.ui.console import CaptureConsole

from lino.adamo.ddl import *

class Foo(StoredDataRow):
    tableName="Foos"
    def initTable(self,table):
        table.addField('value',INT)
        table.addField('name',STRING)
        table.addField('ok',BOOL)

class MySchema(Schema):
    def setupSchema(self):
        self.addTable(Foo)
    #tables=[Foo]

class Case(TestCase):
    
    def test01(self):
        sess = MySchema().createContext()
        q=sess.query(Foo)
        
        try:
            q.appendRow(value=17,ok="no")
            self.fail("failed to raise DataVeto")
        except DataVeto,e:
            pass
        
        try:
            q.appendRow(value=17,name="")
            self.fail("failed to raise DataVeto")
        except DataVeto,e:
            pass
        
        try:
            q.appendRow(value=17,name=" ")
            self.fail("failed to raise DataVeto")
        except DataVeto,e:
            pass
        
        try:
            # strings may not end with a space
            q.appendRow(value=17,name="Foo ")
            self.fail("failed to raise DataVeto")
        except DataVeto,e:
            pass
        
        r1=q.appendRow()
        r2=q.appendRow(value=2,ok=False,name="foofoo")
        r3=q.appendRow(value=3,ok=True,name=None)
        r4=q.appendRow(value=4)

        self.assertEqual(r1,q.peek(1))
        self.assertEqual(r2,q.peek(2))
        self.assertEqual(r3,q.peek(3))
        self.assertEqual(r4,q.peek(4))

        s= str([ r.ok for r in q])
        #print s
        self.assertEqual(s,"[None, False, True, None]")

        r1.lock()
        self.assertEqual(r1.name,None)
        try:
            r1.name=''
            self.fail("failed to raise DataVeto")
        except DataVeto,e:
            pass
        r1.name=None
        self.assertEqual(r1.name,None)
        r1.name="foo"
        self.assertEqual(r1.name,"foo")
        r1.unlock()
        
        #self.assertEqual(r4.name,None)
        
        q.show(width=66)
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""\
Foos
====
value  |name                                      |ok     |id     
-------+------------------------------------------+-------+-------
       |foo                                       |       |1      
2      |foofoo                                    |-      |2      
3      |                                          |X      |3      
4      |                                          |       |4      
        """)
        

if __name__ == '__main__':
    main()

