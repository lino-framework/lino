#coding: latin1
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
   
import sys

from StringIO import StringIO

from lino.misc.tsttools import TestCase

from lino.examples import pizzeria,pizzeria2

from lino.ui import console

def catch_output(f,*args,**kw):
    out = sys.stdout
    sys.stdout = StringIO()
    f(*args,**kw)
    r = sys.stdout.getvalue()
    sys.stdout = out
    return r



class Case(TestCase):
    def test01(self):
        "do the pizzeria examples work?"
        
        self.assertEquivalent(catch_output(pizzeria.main),"""\
Henri must pay 12 EUR
James must pay 53 EUR
""")

    def test02(self):
        "testing pizzeria2"
        self.assertEquivalent(catch_output(pizzeria2.main),"""\
Order #: 3
Date: 20040318
Customer: Bernard
----------------------------------------
Pizza Margerita        1     6
bring home             1     1
----------------------------------------
Total:  7
""")


    def test_voc(self):
        return None # the voc example is sleeping
        from lino.examples import voc
        voc.main()
        

if __name__ == '__main__':
    from unittest import main
    main()

