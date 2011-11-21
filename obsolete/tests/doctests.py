import unittest
import doctest

from lino.misc.my_import import my_import

suite = unittest.TestSuite()
testables=(
   'lino.reports.reports',
    'lino.gendoc.plain',
   )
for modname in testables:
    mod=my_import(modname)
    suite.addTest(doctest.DocTestSuite(mod))
    
runner = unittest.TextTestRunner()
runner.run(suite)
