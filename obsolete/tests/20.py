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


from lino.misc.tsttools import TestCase, main

from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import Nation,Contact
#from lino.reports import DataReport
from lino.adamo.filters import NotEmpty

class Case(TestCase):
    
    def test01(self):
        dbsess = startup()
        be=dbsess.query(Nation).peek("be")
        #qry=be.contacts_by_nation("")
        qry = dbsess.query(Contact,"person.title name",nation=be)
        qry.addColFilter('person',NotEmpty)
        qry.show(columnWidths="12 20")
        #dbc.showQuery(qry,columnWidths="6 10 20")
        #sess.showReport(rpt)
        s = self.getConsoleOutput()
        
        #print s
        
        self.assertEquivalent(s,u"""\
Contacts (nation=Belgium) where 'person' not empty
==================================================
person.title|name
------------+--------------------
Herrn       |Andreas Arens
Monsieur    |Henri Bodard
Herrn       |Emil Eierschal
Frau        |Erna Eierschal
Herrn       |Gerd Großmann
Herrn       |Frédéric Freitag
""")
                         

        dbsess.shutdown()

if __name__ == '__main__':
    main()

