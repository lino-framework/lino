## Copyright 2005-2007 Luc Saffre

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

import os
import sys

from lino.misc.tsttools import TestCase, main

from lino.tools.months import Month
from lino.tools.anyrange import anyrange
from lino.tools.indexing_be import indexed_price
from lino.tools.fixedpoint import FixedPoint

class Case(TestCase):

    def test01(self):
        
        l = [str(m) for m in anyrange(Month(2003,10),Month(2004,02),1)]
        s=" ".join(l)
        #print s
        self.assertEqual(s,"10/2003 11/2003 12/2003 01/2004 02/2004")
        
        m0 = m = Month(2003,3)
        self.assertEqual(m,Month(2003,3))
        
        m += 1
        self.assertEqual(m,Month(2003,4))

        m2 = m+1
        self.assertEqual(m2,Month(2003,5))
        
        i = Month(2005,6) - Month(2003,6)
        self.assertEqual(i,24)
        
        i = Month(2005,6) - Month(2003,4)
        self.assertEqual(i,26)
        
        i = Month(2005,6) - Month(2003,7)
        self.assertEqual(i,23)
        
        i = Month(2005,6) - Month(2005,6)
        self.assertEqual(i,0)

        i = Month(2002,8) - Month(1994,1)
        self.assertEqual(i,103) # 103=8*12+7
        
        i = Month(2005,5) - Month(1994,1)
        self.assertEqual(i,136) # 136=11*12+4
        
        
        
    def test02(self):
        
        # same results as with
        # http://www.snp-aes.be/AES_CDML/DefaultFr.htm
        # or
        # http://mineco.fgov.be/informations/statistics/indicators/rent_fr.asp

        def check(base,target,p1,p2):
            p=indexed_price(base,target,p1)
            self.assertEqual(p,FixedPoint(p2))
        
        # base 1996
        
        check(200208,200505, 300, 315.49)
        check(200208,200505, 400, 420.65)
        check(200208,200505, 500, 525.82)
        check(200208,200505, 600, 630.98)
        check(200208,200505, 750, 788.73)
        check(200208,200505, 2200, 2313.60)
        
        check(200208,200601, 300, 317.91)
        check(200208,200601, 400, 423.88)
        check(200208,200601, 500, 529.85)
        check(200208,200601, 600, 635.82)
        check(200208,200601, 750, 794.77)
        check(200208,200601, 792, 839.28)
        check(200208,200601, 2200, 2331.33)
        
        check(200208,200606,  100,  107.11)
        check(200208,200606,  200,  214.22)
        check(200208,200606,  300,  321.33)
        check(200208,200606,  400,  428.44)
        check(200208,200606,  500,  535.56)
        check(200208,200606,  600,  642.67)
        check(200208,200606,  750,  803.33)
        check(200208,200606,  792,  848.32)
        check(200208,200606, 2200, 2356.45)
        
        check(200208,200701,  1000,  1081.35)
        check(200208,200701,  750,  811.01)
        check(200208,200701, 1250, 1351.68)
        check(200208,200702, 400, 434.75)
        check(200208,200702, 500, 543.44)

        check(200208,200705, 400, 434.28)
        check(200208,200706, 1050, 1139.32)
        check(200208,200706, 1000, 1085.06)
        
        check(200208,200711, 750, 826.50)
        check(200208,200711, 600, 661.20)
        check(200208,200711, 500, 551.00)
        
        #base 2004:
        
        check(200610,200701, 1250, 1257.27)
        
        #base 1988:
        
        check(199203,200601, 100, 126.21)
        
    
if __name__ == '__main__':
    main()

