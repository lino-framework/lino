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
using lino.reports on pizzeria
"""

from lino.misc.tsttools import TestCase, main


class Case(TestCase):


    def test01(self):
        from lino.examples.pizzeria2 import beginSession,\
             Products, OrderLines
        sess = beginSession()
        PROD = sess.query(Products)
        q = sess.query(OrderLines,"ordr.date ordr.customer",
                       product=PROD.peek(1))
        rpt = self.ui.report()
        q.setupReport(rpt,columnWidths="10 10")
        rpt.execute(q)
        s = self.getConsoleOutput()
        #print s
        self.assertEqual(s,"""\
OrderLines
==========
date      |customer  
----------+----------
2003-08-16|Henri     
2003-08-16|James     
2004-03-18|Bernard   
2004-03-19|Henri     
""")        
        
        

if __name__ == '__main__':
    main()

