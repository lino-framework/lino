import shelve
import os
import os.path
#import sys
import unittest
import shutil

#sys.path.append("..")
#from lino import pickle_dbd
#from lino.demoapp import DemoApp

from lino.misc.tsttools import TestCase

#from lino.tools import *

class Dummy:
   def __init__(self,name,age):
      self.name = name
      self.age = age

class MyCase(TestCase):
   
   def test01(self):
      "basic operations directly on a shelve"

      ## The optional flag argument can be 'r' (to open an existing
      ## database for reading only -- default), 'w' (to open an
      ## existing database for reading and writing), 'c' (which
      ## creates the database if it doesn't exist), or 'n' (which
      ## always creates a new empty database).
      
      filename = os.path.join("tmp","2","test") # + ".db"

      # just create the file:
      db = shelve.open(filename,"n")
      assert len(db) == 0
      db.close()

      # a little bit later we open it to write some data
      db = shelve.open(filename,"w")
      for i in range(0,1000):
         db[str(i)] = Dummy("foo",i)
      db.close()
      
      # again a little bit later...
      db = shelve.open(filename,"w")
      self.assertEqual(len(db),1000)

      dummy = db['123']
      self.assertEqual(dummy.name,"foo")
      db['234'] = Dummy("replace",234)
      db.close()

   def test02(self):
      "basic operations directly on a pickle"
      from cPickle import dump,load
      filename = os.path.join("tmp","2","test") + ".db"
      db = {}
      for i in range(0,1000):
         db[i] = Dummy("foo",i)
      f = open(filename,"wb")
      dump(db,f,1)
      f.close()

      f = open(filename,"rb")
      db = load(f)
      f.close()
      self.assertEqual(len(db),1000)
      dummy = db[123]
      self.assertEqual(dummy.name,"foo","r")
      
   def test03(self):
      import anydbm
      filename = os.path.join("tmp","2","test") + ".db"
      db = anydbm.open(filename,"n")
      db["1"] = 'bar'
      db.close()

      db = anydbm.open(filename,"w")
      self.failUnless(db.has_key("1"))
      
      db["2"] = 'foo'
      ## db.sync()

##       k = db.first()
##       while k != None:
##          print k
##          k = db.next(k)


      
   def setUp(self):
      self.tmpDir = os.path.join("tmp","2")
      if not os.path.exists(self.tmpDir):
         os.makedirs(self.tmpDir)
      
   def tearDown(self):
      shutil.rmtree(self.tmpDir)
      
      
      
def suite():
    l = [
        unittest.makeSuite(MyCase),
    ]
    return unittest.TestSuite(l)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
 

