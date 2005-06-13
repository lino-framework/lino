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
- loop through partners in Belgium, setting currency to EUR 
- test for equality of DataRow instances


"""
from lino.misc.tsttools import TestCase, main
from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Partners, Currencies, Nations

class Case(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.db = demo.startup()

    def tearDown(self):
        self.db.shutdown()


    def test01(self):
        NATIONS = self.db.query(Nations)
        CURR = self.db.query(Currencies)
        PARTNERS = self.db.query(Partners)
        be = NATIONS.peek("be")
        BEF = CURR.peek('BEF')
        EUR = CURR.peek('EUR')
        s = ""
        for p in PARTNERS.query("currency",
                                        orderBy="name firstName",
                                        nation=be):
            #if p.currency is None:
            #   s += p.__str__() + " : currency remains None\n"
            if p.currency != EUR:
                # print p, p.currency.id
                s += p.__str__() + " : currency %s updated to EUR\n" % str(p.currency)
                p.lock()
                p.currency = EUR
                p.unlock()
            else:
                s += p.__str__() + " : currency was already EUR\n"

        #print s
        self.assertEqual(s,"""\
Andreas Arens : currency BEF updated to EUR
Henri Bodard : currency BEF updated to EUR
Emil Eierschal : currency was already EUR
Erna Eierschal : currency was already EUR
Frédéric Freitag : currency None updated to EUR
Gerd Großmann : currency was already EUR
PAC Systems PGmbH : currency None updated to EUR
""")
        
        


if __name__ == '__main__':
    main()

