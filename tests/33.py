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

from lino.forms.session import Session

from lino import i18n
i18n.setUserLang(None)

class Case(TestCase):

    verbosity=1
    
    def test01(self):
        #
        #sess=Session(Toolkit())
        #sess=syscon._session
        job=syscon.job("Testing uncomplete jobs",10)
        for i in range(5):
            job.increment()
        job.done("done in only 5 steps.")
        s=self.getConsoleOutput()
        #print s
        self.assertEquivalent(s,"""
Testing uncomplete jobs
[ 10%] Working
[ 20%] Working
[ 30%] Working
[ 40%] Working
[ 50%] Working
[100%] Working
Testing uncomplete jobs: done in only 5 steps.
""")
        

if __name__ == '__main__':
    main()

