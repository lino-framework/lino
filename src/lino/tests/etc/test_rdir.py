import os
from unittest import TestCase
from lino.misc import rdir

class MyCase(TestCase):
   
   def test01(self):
      "testing rdir"
      l1 = rdir.rdirlist()
      cwd = os.getcwd()
      os.chdir('..')
      l2 = rdir.rdirlist(cwd)
      os.chdir(cwd)
      self.assertEqual(l1,l2)

      
 


