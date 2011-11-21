# coding: latin1
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
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import *
from lino.adamo.filters import NotEmpty
#from lino.apps.addrbook import demo
#from lino.apps.addrbook.tables import Partner

class Case(TestCase):

        
    def test01(self):
        db = startup()
        s1 = ''
        q = db.query(Contact,\
                     "name street city.name",
                     orderBy="name")
        q.addColFilter('city',NotEmpty)
##         for row in q:
##             #print row[0]
##             s1 += str(row[0]) + " "
##             s1 += str(row[1]) + " "
##             s1 += str(row[2]) + "\n"
##         #print s1
##         self.assertEqual(s1,"""\
## Arens None Eupen
## Ausdemwald None Aachen
## Bodard None Verviers
## Eesti Telefon Sõpruse pst. Tallinn
## Eierschal None Eupen
## Eierschal None Eupen
## Freitag None Eupen
## Girf OÜ Laki Tallinn
## Großmann None Eupen
## PAC Systems PGmbH Hütte Eupen
## Rumma & Ko OÜ Tartu mnt. Tallinn
## Saffre None Tallinn
## """)

        
        s2 = ''
        for row in q:
            s2 += unicode(row.name) + " "
            if row.street is not None:
                s2 += unicode(row.street) + " "
            s2 += unicode(row.city.name) + "\n"

        #print s2
        
        self.assertEquivalent(s2,u"""\
Andreas Arens Eupen
Anton Ausdemwald Aachen
Emil Eierschal Eupen
Erna Eierschal Eupen
Frédéric Freitag Eupen
Gerd Großmann Eupen
Hans Flott Bierstraße München
Henri Bodard Verviers
Kati Kask Tallinn
Kurtz & Büntig Bergstraße Eupen
Mets & puu OÜ Tartu mnt. Tallinn
Reisebüro Freitag Hütte Eupen
Tõnu Tamm Tallinn        
""")

        # some other cases (for example 80.py) would fail if run
        # together with this case in one suite and if the following
        # lines were not:
        
        db.shutdown()

if __name__ == '__main__':
    main()

