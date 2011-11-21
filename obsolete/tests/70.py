#----------------------------------------------------------------------
# Copyright 2003-2004 Luc Saffre
# This file is published as part of the Lino project
#----------------------------------------------------------------------

import os

from lino.misc import tsttools
#from lino.scripts.webman import main

class Case(tsttools.TestCase):
    todo="scripts/webman is broken"

    def test01(self):
        main([os.path.join("testdata","webman")])
        

if __name__ == '__main__':
    tsttools.main()

