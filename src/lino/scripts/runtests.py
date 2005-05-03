"""
scan a directory tree for .py files containing test cases and run them
"""

import sys
import unittest

from lino.misc import tsttools
from lino.ui import console 

class Runtests(console.ConsoleApplication):

    name="Lino/runtests"
    years='2004-2005'
    author='Luc Saffre'
    
    usage="usage: %prog [options] [TESTS]"
    
    description="""\
where TESTS specifies the tests to run. Default is all. Other possible values e.g. `1` or `1-7` 
"""
    
##     def run(self,ui):
##         suite = tsttools.alltests(self.args)
##         runner = unittest.TextTestRunner()
##         runner.run(suite)
        
    def run(self,ui):
        tests = tsttools.collectTestCases(ui,self.args)
        runner = unittest.TextTestRunner(verbosity=1)
        for t in tests:
            result=runner.run(t)
            if not result.wasSuccessful():
                return -1


# lino.runscript expects a name consoleApplicationClass
consoleApplicationClass = Runtests

if __name__ == '__main__':
    consoleApplicationClass().main() # console,sys.argv[1:])
    


## def main(args):
##     Runtests().main(console,args)

## if __name__ == "__main__":
##     main(sys.argv[1:])



