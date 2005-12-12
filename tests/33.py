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

import types
from lino.misc.tsttools import TestCase, main, Toolkit
from lino.console import syscon

#from lino.forms.session import Session
#from lino.console.task import Task
from lino.console.task import Task

#from lino import i18n
#i18n.setUserLang(None)

## class TestTask(Task):
    
##     maxval=10
    
##     def getLabel(self):
##         return "Testing uncomplete tasks"
    

class Case(TestCase):

    verbosity=1
    
    def test01(self):

        def func(task):
            task.session.notice("Running...")
            for i in range(5):
                for c in "abc":
                    task.session.notice("Performing step %d%s)",i+1,c)
                task.increment()
            task.session.notice("Done in only 5 steps.")

        syscon.loop(func,"Testing uncomplete tasks",10)
        

        
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
##         self.assertEquivalent(s,"""
## Testing uncomplete tasks
## [  0%] Running...
## [  0%] Performing step 1a)
## [  0%] Performing step 1b)
## [  0%] Performing step 1c)
## [ 10%] Performing step 1c)
## [ 10%] Performing step 2a)
## [ 10%] Performing step 2b)
## [ 10%] Performing step 2c)
## [ 20%] Performing step 2c)
## [ 20%] Performing step 3a)
## [ 20%] Performing step 3b)
## [ 20%] Performing step 3c)
## [ 30%] Performing step 3c)
## [ 30%] Performing step 4a)
## [ 30%] Performing step 4b)
## [ 30%] Performing step 4c)
## [ 40%] Performing step 4c)
## [ 40%] Performing step 5a)
## [ 40%] Performing step 5b)
## [ 40%] Performing step 5c)
## [ 50%] Performing step 5c)
## [ 50%] Done in only 5 steps.
## [100%] Done in only 5 steps.
## 0 warnings
## 0 errors
## """)
        

if __name__ == '__main__':
    main()

