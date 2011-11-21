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

This is to test whether the schema of each application initializes
correctly.

see also :
test 81 does a demo.startup() of all these applications

"""

import os
from lino.misc.tsttools import TestCase, main
from lino import scripts


class Case(TestCase):
    
    def test01(self):
        scriptsdir=scripts.__path__[0]
        for fn in scripts.__all__:
            pfn= os.path.join(scriptsdir,fn)+".py"
            if not os.path.exists(pfn):
                self.fail(pfn+" : no such file")
        

if __name__ == '__main__':
    main()

