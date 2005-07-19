## Copyright 2005 Luc Saffre

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
        base=itom(200208)
        now=itom(200505)
        p=indexed_price(400,base,now)
        self.assertEqual(int(p*100),42065)
        p=indexed_price(500,base,now)
        self.assertEqual(int(p*100),52581)
        p=indexed_price(600,base,now)
        self.assertEqual(int(p*100),63098)
        p=indexed_price(750,base,now)
        self.assertEqual(int(p*100),78872)
        p=indexed_price(2200,base,now)
        self.assertEqual(int(p*100),231359)
        
        
        
    
if __name__ == '__main__':
    main()

