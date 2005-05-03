import unittest


class C:
	def m1(self,a):
		return "m1(%s)" % repr(a)

class MyCase(unittest.TestCase):

   def test01(self):

		def foo(c,a):
			return "m2(%s)" % repr(a)

		setattr(C,'m2',foo)

		c = C()

		self.assertEqual(c.m1(3),"m1(3)")
		self.assertEqual(c.m2(3),"m2(3)")
		#self.assertEqual(c.m2(3),"m3(3)")
		

		
if __name__ == '__main__':
	unittest.main()

