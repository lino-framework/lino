import unittest
import sys,os

from gandalf.misc import tsttools


if __name__ == "__main__":
   suite = tsttools.alltests(sys.argv[1:])
   runner = unittest.TextTestRunner()
   runner.run(suite)
   
