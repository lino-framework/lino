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

import os
import sys

from lino.misc.tsttools import TestCase, main

from lino.tools.months import Month
from lino.tools.anyrange import anyrange
from lino.tools.indexing_be import indexed_price
from lino.adamo.datatypes import stom, itom


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

        def check(base,now,p1,p2):
            p=indexed_price(p1,base,now)
            self.assertEqual(round(p,2),round(p2,2))
        
        base=itom(200208) # base 1996
        
        now=itom(200505)

        check(base,now, 300, 315.49)
        check(base,now, 400, 420.65)
        check(base,now, 500, 525.82)
        check(base,now, 600, 630.98)
        check(base,now, 750, 788.73)
        check(base,now, 2200, 2313.60)
        
        now=itom(200601)
        
        check(base,now, 300, 317.91)
        check(base,now, 400, 423.88)
        check(base,now, 500, 529.85)
        check(base,now, 600, 635.82)
        check(base,now, 750, 794.77)
        check(base,now, 2200, 2331.33)
        
        #base 1988
        check(itom(199203),itom(200601), 100, 126.21)
        
    
if __name__ == '__main__':
    main()

