import unittest
import sys

from lino.misc import tsttools


if __name__ == "__main__":
   suite = tsttools.alltests(argv=sys.argv[1:])
   runner = unittest.TextTestRunner()
   runner.run(suite)
   


