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

from lino.misc.tsttools import TestCase, main, catch_output
from lino.misc.my_import import my_import
from lino.apps import timtools

# same list as in mkdist.py
console_targets = timtools.console_targets()
## [
##     'pds2pdf',
##     'pds2sxw', 'pds2sxc',
##     'prn2pdf', 'prnprint',
##     'sync', 'diag',
##     'openmail', 'openurl'
##     ]


class Case(TestCase):
    def test01(self):
        s = ""
        for scr in console_targets:



            cmd="lino "+scr+" --help"
            fd=os.popen(cmd,"r")
            observed=fd.read()
            msg="lino %s failed" % scr
            self.assertEqual(fd.close(),None,msg)
            outfile=os.path.join("testdata","timtools",scr)+".help.txt"
            expected=open(outfile).read()
            self.assertEquivalent(observed,expected,msg)

##             mod = my_import("lino.scripts." + scr)
##             self.failUnless(hasattr(mod,"consoleApplicationClass"),scr)
##             main=mod.consoleApplicationClass.main
##             s += catch_output(mod.main,[])
            #mod.main(["--help"])

        #s = self.getConsoleOutput()
        #print s
        #self.assertEquivalent(s,"")
        
    
    
if __name__ == '__main__':
    main()

