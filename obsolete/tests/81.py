#coding: latin1
## Copyright 2003-2006 Luc Saffre

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
"""
from lino.misc.tsttools import TestCase, main

class Case(TestCase):

    def doit(self,sess,expected):
        vetos=[]
        for t in sess.getTableList():
            q=sess.query(t._instanceClass)
            for row in q:
                msg=row.vetoDelete()
                if msg:
                    vetos.append(msg)
        self.assertEquivalent("\n".join(vetos),expected)
        sess.shutdown()
    
    def test01(self):
        from lino.apps.contacts.contacts_demo import startup
        self.doit(startup(), u"""
Estonia is used by 10 rows in Cities
Belgium is used by 9 rows in Cities
Germany is used by 7 rows in Cities
Eupen (be) is used by 7 rows in Contacts
Verviers (be) is used by 1 rows in Contacts
Aachen (de) is used by 1 rows in Contacts
München (de) is used by 1 rows in Contacts
Tallinn (ee) is used by 3 rows in Contacts
Kurtz & Büntig is used by 3 rows in Contacts
Reisebüro Freitag is used by 2 rows in Contacts
Bäckerei Ausdemwald is used by 1 rows in Contacts
Hans Flott is used by 2 rows in Contacts
Mets & puu OÜ is used by 2 rows in Contacts
Andreas Arens is used by 1 rows in Contacts
Anton Ausdemwald is used by 2 rows in Contacts
Emil Eierschal is used by 1 rows in Contacts
Henri Bodard is used by 1 rows in Contacts
Erna Eierschal is used by 1 rows in Contacts
Gerd Großmann is used by 1 rows in Contacts
Frédéric Freitag is used by 2 rows in Contacts
Tõnu Tamm is used by 1 rows in Contacts
Kati Kask is used by 2 rows in Contacts
Klaus Kurtz is used by 1 rows in Contacts
Bruno Büntig is used by 1 rows in Contacts
Hans Flott is used by 1 rows in Contacts
Director is used by 6 rows in Contacts        
        """)
        
    def test02(self):
        from lino.apps.pinboard.pinboard_demo import startup
        self.doit(startup(), """\
Estonia is used by 10 rows in Cities
Belgium is used by 9 rows in Cities
Germany is used by 7 rows in Cities
English is used by 7 rows in Quotes
German is used by 1 rows in Quotes
French is used by 1 rows in Quotes
Project 1 is used by 3 rows in Projects
Project 1.3 is used by 2 rows in Projects
Project 1.3.2 is used by 2 rows in Projects
Georges Brassens is used by 1 rows in Quotes
Anonymus is used by 4 rows in Quotes
Peter Lauster is used by 1 rows in Quotes
Henry Louis Mencken is used by 2 rows in Quotes
Winston Churchill is used by 1 rows in Quotes        
        """)
        
    def test03(self):
        from lino.apps.ledger.ledger_demo import startup
        self.doit(startup(), u"""\
BEF is used by 8 rows in Contacts
Chair is used by 1 rows in InvoiceLines
Table is used by 1 rows in InvoiceLines
outgoing invoices is used by 1 rows in Invoices
OUT-1 is used by 2 rows in InvoiceLines
Estonia is used by 10 rows in Cities
Belgium is used by 9 rows in Cities
Germany is used by 7 rows in Cities
Eupen (be) is used by 7 rows in Contacts
Verviers (be) is used by 1 rows in Contacts
Aachen (de) is used by 1 rows in Contacts
München (de) is used by 1 rows in Contacts
Tallinn (ee) is used by 3 rows in Contacts
Kurtz & Büntig is used by 3 rows in Contacts
Reisebüro Freitag is used by 2 rows in Contacts
Bäckerei Ausdemwald is used by 1 rows in Contacts
Hans Flott is used by 2 rows in Contacts
Mets & puu OÜ is used by 2 rows in Contacts
Andreas Arens is used by 1 rows in Contacts
Anton Ausdemwald is used by 2 rows in Contacts
Emil Eierschal is used by 1 rows in Contacts
Henri Bodard is used by 1 rows in Contacts
Erna Eierschal is used by 1 rows in Contacts
Gerd Großmann is used by 1 rows in Contacts
Frédéric Freitag is used by 2 rows in Contacts
Tõnu Tamm is used by 1 rows in Contacts
Kati Kask is used by 2 rows in Contacts
Klaus Kurtz is used by 1 rows in Contacts
Bruno Büntig is used by 1 rows in Contacts
Hans Flott is used by 1 rows in Contacts
Director is used by 6 rows in Contacts        
        """)
        
if __name__ == '__main__':
    main()

