# -*- coding: Latin-1 -*-
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

from lino.misc.tsttools import TestCase, main
from lino.adamo.ddl import *

class Case(TestCase):
    
    def test01(self):

        okValues = {
            INT: (-1, 0, 1, 20000),
            LONG: (-1L, 0L, 1L, 20000L, 12345678901234567890L),
            BOOL: (True,False),
            }

        badValues = {
            LONG: (True,-1,0,1,20000),
            INT: (False,-1L,0L,1L,20000L,12345678901234567890L),
            DATE: (1,'',1L,True),
            BOOL: ("yes", 0, 1),
            }

        for k,vlist in okValues.items():
            for v in vlist:
                k.validate(v)

        for k,vlist in badValues.items():
            for v in vlist:
                try:
                    k.validate(v)
                    self.fail(
                        "%s failed to reject bad value %r" % (k,v))
                except DataVeto,e:
                    pass
                
        
if __name__ == '__main__':
    main()

