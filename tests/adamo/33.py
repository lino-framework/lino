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
Some tests on getDemoDB()
"""

import types
#import unittest
from lino.misc.tsttools import TestCase, main

#from lino.ui import console


class Case(TestCase):


    def test01(self):
        #
        d = dict(
            name="Ausdemwald",
            firstName="Norbert",
            size=12,
            description="""Norbert ist unser treuer Mitarbeiter im Vurt. Er wohnt in der Fremereygasse in Eupen."""
            )
        
        #console.startDump()
        rpt = self.ui.report()
        rpt.addColumn(meth=lambda row: str(row[0]),
                      label="key",
                      width=12)
        rpt.addColumn(meth=lambda row: repr(row[1]),
                      label="value",
                      width=40)
        rpt.execute(d.items())
        s = self.getConsoleOutput()
        #print s
        self.assertEqual(s,"""\
key         |value                                   
------------+----------------------------------------
size        |12                                      
name        |'Ausdemwald'                            
firstName   |'Norbert'                               
description |'Norbert ist unser treuer Mitarbeiter im
            |Vurt. Er wohnt in der Fremereygasse in  
            |Eupen.'                                 
""")        
        
        

if __name__ == '__main__':
    main()

