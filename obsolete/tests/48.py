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
from lino.misc.tsttools import TestCase, main

class Case(TestCase):
    def test01(self):
    
        s = ""
        fn=os.path.join("testdata",'cp850box.txt')
        for line in file(fn).readlines():
            line = line.strip().decode('cp850')
            for c in line:
                if c == " ":
                    s += "     "
                else:
                    s += "%x " % ord(c) 
            s += "\n"
            
        #print s
        self.assertEqual(s,"""\
250c 2500 252c 2510 
2502      2502 2502 
251c 2500 253c 2524 
2514 2500 2534 2518 

2554 2550 2566 2557 
2551      2551 2551 
2560 2550 256c 2563 
255a 2550 2569 255d 
""")
    
if __name__ == '__main__':
    main()

