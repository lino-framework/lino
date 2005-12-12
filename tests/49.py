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

#from lino.misc.tsttools import TestCase, main, catch_output
from lino.misc.tsttools import TestCase, main, DOCROOT
from lino.misc.my_import import my_import
from lino.apps import timtools

# same list as in mkdist.py
console_targets = timtools.console_targets()

class Case(TestCase):
    def test01(self):
        s = ""
        for script in console_targets:

            cmd="lino "+script+" --help"
            fd=os.popen(cmd,"r")
            observed=fd.read()
            fn=os.path.join(DOCROOT,"help",script)+".help.txt"
            msg="output of `%s` differs from content of %s" % (cmd,fn)
            self.assertEqual(fd.close(),None,msg)
            expected=open(fn).read()
            self.assertEquivalent(observed,expected,msg)

    
    
if __name__ == '__main__':
    main()

