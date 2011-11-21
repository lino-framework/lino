#----------------------------------------------------------------------
# Copyright 2003-2004 Luc Saffre
# This file is published as part of the Lino project
#----------------------------------------------------------------------

"""
testing restify.inspect()
"""
import os

from lino.misc import tsttools
from lino.misc.restify import inspect

class Case(tsttools.TestCase):
    ""
    todo="restify.inspect() doesn't use filename"

    def test01(self):
        doc = inspect(os.path.join("testdata","webman","index.txt"))
        print repr(doc.get_children())
        

if __name__ == '__main__':
    tsttools.main()

