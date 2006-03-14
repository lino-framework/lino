# coding: latin1
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


"""

Deciding whether to store values of a DataRow in a tuple of atomic
values or in a dict of complex values...

1. I iterate over a PARTNERS query with only the "currency" column
   (because this is the only one I am going to use. Plus the implicit
   "nation" column.

   The "print p" statement will do a call to Partners.getRowLabel()
   which will access row.name --- a field that was not included in my
   columnNames!

   Or if I modify the row, then the validateRow() action will be
   triggered and it will ask for the partner's name.

   If a field was not part of the initial query, it will silently be
   looked up.

2. Accessing p.nation.name means that an attribute "p.nation" exists
   and has a Nations row as value.

3. (new:) Iterating over a row returns the cell value for each visible
   column of its query.



"""
from lino.misc.tsttools import TestCase, main

from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import Nation,Partner
#from lino.reports import DataReport

class Case(TestCase):
    
    def test01(self):
        dbsess = startup()
        be = dbsess.query(Nation).peek("be")
        qry = dbsess.query(Partner,
                           "title firstName name",
                           nation=be)
        qry.showReport(columnWidths="6 10 20")
        #dbc.showQuery(qry,columnWidths="6 10 20")
        #sess.showReport(rpt)
        s = self.getConsoleOutput()
        
        #print s
        
        self.assertEquivalent(s,u"""\
Partners (nation=Belgium)
=========================
title |firstName |name                
------+----------+--------------------
Herrn |Andreas   |Arens               
Dr.   |Henri     |Bodard              
Herrn |Emil      |Eierschal           
Frau  |Erna      |Eierschal           
Herrn |Gerd      |Großmann            
Herrn |Frédéric  |Freitag             
      |          |PAC Systems PGmbH   
""")
                         

        # some other cases (for example 80.py) would fail if run
        # together with this case in one suite and if the following
        # line were not:
        
        dbsess.shutdown()

if __name__ == '__main__':
    main()

