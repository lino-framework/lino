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
#from lino.ui.console import CaptureConsole

class Case(TestCase):
    
    skip=True
    
    def test01(self):
        
        def f(con,maxval):
            job = con.job("Gonna do it", maxval=maxval*2)
            job.notice("First part")
            for i in range(maxval):
                job.increment()
            job.notice("Second part")
            for i in range(maxval):
                job.increment()
            job.done()
            return con.getConsoleOutput()

        # very quiet console:
        c = CaptureConsole()
        c.parse_args('-qq'.split())
        #self.assertEqual(f(c,3),"")
        
        # quiet console:
        c = CaptureConsole()
        c.parse_args('-q'.split())
        #self.assertEqual(f(c,3),"Gonna do it...")
        
        # normal console:
        c = CaptureConsole()
        self.assertEquivalent(f(c,3),"""\
Gonna do it...
First part... [100%]
Second part... [100%]
""")

        # "verbose" and "debug" are same as "normal"
        

if __name__ == '__main__':
    main()

