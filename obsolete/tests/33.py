# coding: latin1

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

from lino.misc.tsttools import TestCase, main

from lino.console.task import Progresser

class TestTask(Progresser):
    
    maxval=10
    name="Testing uncomplete tasks"
    
    def run(self):
        self.notice("Running...")
        for i in range(5):
            for c in "abc":
                self.notice("Performing step %d%s)",i+1,c)
            self.increment()
        self.notice("Done in only 5 steps.")


class Case(TestCase):

    verbosity=1
    
    def test01(self):

        self.toolkit.runtask(TestTask())

        #syscon.runTask(TestTask())
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""
Testing uncomplete tasks
Running...
Performing step 1a)
Performing step 1b)
Performing step 1c)
Performing step 2a)
Performing step 2b)
Performing step 2c)
Performing step 3a)
Performing step 3b)
Performing step 3c)
Performing step 4a)
Performing step 4b)
Performing step 4c)
Performing step 5a)
Performing step 5b)
Performing step 5c)
Done in only 5 steps.
""")
        

if __name__ == '__main__':
    main()

