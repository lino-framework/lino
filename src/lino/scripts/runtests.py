"""
scan a directory for .py files containing test cases and run these
"""

import sys
import unittest

from lino.misc import tsttools
from lino.ui import console

def main(argv):

    console.set(verbosity=-1)
    
    parser = console.getOptionParser(
        usage="usage: %prog [options] [TESTS]",
        description="""\
where TESTS specifies the tests to run. Default is all. Other possible values e.g. `1` or `1-7` 
""")
    
    
    (options, args) = parser.parse_args(argv)
    
##     if console.isInteractive():
##         console.warning("""\
## Note: Running in interactive mode. Specify -b to avoid questions.""")
        
    suite = tsttools.alltests(args)
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    main(sys.argv[1:])



