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
    
    #def main(self,argv):

    #syscon.set(verbosity=-2)
    
##     parser = syscon.getOptionParser(
##         usage="usage: %prog [options] [TESTS]",
##         description="""\
## where TESTS specifies the tests to run. Default is all. Other possible values e.g. `1` or `1-7` 
## """)
    
    
    #(options, args) = syscon.parse_args(argv)
    
    
##     if console.isInteractive():
##         console.message("""\
## Note: Running in interactive mode. Specify -b to avoid questions.""")

    
    def run(self,ui):
        suite = tsttools.alltests(self.args)
        runner = unittest.TextTestRunner()
        runner.run(suite)


# lino.runscript expects a name consoleApplicationClass
consoleApplicationClass = Runtests

if __name__ == '__main__':
    consoleApplicationClass().main() # console,sys.argv[1:])
    


## def main(args):
##     Runtests().main(console,args)

## if __name__ == "__main__":
##     main(sys.argv[1:])



