# coding: latin1
#----------------------------------------------------------------------
# Copyright: (c) 2003-2004 Luc Saffre
# License:   GPL
#----------------------------------------------------------------------

"""
testing restify.inspect()
"""
import unittest

from lino.misc.restify import inspect

class Case(unittest.TestCase):
    ""

    def test01(self):
        doc = inspect("index.txt")
        print repr(doc.get_children())
        

if __name__ == '__main__':
    unittest.main()

