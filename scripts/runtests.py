"""
scan a directory for .py files containing test cases and run these
"""

import unittest
from lino.misc import tsttools

def main(args):
   suite = tsttools.alltests(args)
   runner = unittest.TextTestRunner()
   runner.run(suite)

if __name__ == "__main__":
	import sys
	from lino.misc import console
	console.getSystemConsole().set(batch=True)
	main(sys.argv[1:])



