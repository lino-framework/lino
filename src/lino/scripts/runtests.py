"""
scan a directory tree for .py files containing test cases and run them
"""

import sys
import unittest

from lino.misc import tsttools
from lino.ui import console as syscon

def main(argv):

    syscon.set(verbosity=-2)
    
    parser = syscon.getOptionParser(
        usage="usage: %prog [options] [TESTS]",
        description="""\
where TESTS specifies the tests to run. Default is all. Other possible values e.g. `1` or `1-7` 
""")
    
    
    (options, args) = parser.parse_args(argv)
    
##     if console.isInteractive():
##         console.message("""\
## Note: Running in interactive mode. Specify -b to avoid questions.""")
        
    suite = tsttools.alltests(args)
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    main(sys.argv[1:])



