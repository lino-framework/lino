import unittest

class Component:
   def __init__(self,name):
      self.name = name
      
class Row:

   def __init__(self):
      self.__dict__["_values"] = {}

   def __getattr__(self,name):
      try:
         return self.__dict__["_values"][name]
         #return self._values[name]
      except KeyError,e:
         raise AttributeError,str(e)
   
   def __setattr__(self,name,value):
      self.__dict__["_values"][name] = value

   

class MyCase(unittest.TestCase):
   def setUp(self):
      self.comps = []
      self.comps.append(Component("a"))
      self.comps.append(Component("b"))
      self.comps.append(Component("c"))
      
   def test_2(self):
      self.assertEqual(self.FindCompIndex("b"),1)

   def test_3(self):
      """
         testing a Row instance for equality with None raises
         TypeError: 'NoneType' object is not callable

         Strange! Of course is 'None' not callable! Who told you to
         call it?
         
      """
      row = Row()
      row.a = "a" # this works
      if row == None: # here it happens.
         print "row instance is None!"

   def FindCompIndex(self,name):
      i = 0
      for comp in self.comps:
         if comp.name == name:
            return i
         i+= 1
         


def suite():
    l = [
        unittest.makeSuite(MyCase),
    ]
    return unittest.TestSuite(l)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
 

