import unittest

from lino.misc.expose import expose

class A:
   def __init__(self,name):
      self.name = name
      
   def f1(self):
      return '%s.f1()' % self.name
   
class B(A):
   
   def f1(self):
      return '%s.f1()' % self.name
   
   def f2(self):
      return '%s.f2()' % self.name

class C(B):
   
   def f1(self):
      return '%s.f1()' % self.name
   
   def f2(self):
      return '%s.f2()' % self.name

   def f3(self):
      return '%s.f3()' % self.name


   
class Case(unittest.TestCase):
   
   def test01(self):
      a = A("a")
      b = B("b")
      c = C("c")

      names = expose(a)

      self.assertEqual(a.f1(),eval("f1()",names))

      names = expose(b)
      self.assertEqual(b.f1(),eval("f1()",names))
      self.assertEqual(b.f2(),eval("f2()",names))
      
      names = expose(c)
      self.assertEqual(c.f1(),eval("f1()",names))
      self.assertEqual(c.f2(),eval("f2()",names))
      self.assertEqual(c.f3(),eval("f3()",names))
      
      

      

      
if __name__ == '__main__':
   unittest.main()
 

