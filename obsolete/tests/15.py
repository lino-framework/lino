import unittest
from lino.tools.normalDate import ND

class Case(unittest.TestCase):
		
	def test01(self):
		self.assertEqual(str(ND(20040101)-1),'20031231')
		self.assertEqual(str(ND(20040305)-5),'20040229')
		
		self.assertEqual(ND(20040325)-ND(20040324),1)
		self.assertEqual(ND(20040325)-ND(20040301),24)
		self.assertEqual(ND(20040325)-ND(20040229),25)
		self.assertEqual(ND(20040325)-ND(20040222),32)
		
		self.assertEqual(ND(20040101).dayOfWeek(),3) # thu
		self.assertEqual(ND(20030101).dayOfWeek(),2) # wed
		self.assertEqual(ND(20020101).dayOfWeek(),1) # tue
		self.assertEqual(ND(20010101).dayOfWeek(),0) # mon
		self.assertEqual(ND(20000101).dayOfWeek(),5) # sat
		self.assertEqual(ND(19990101).dayOfWeek(),4) # fri
		self.assertEqual(ND(19950101).dayOfWeek(),6) # sun
		
		self.assertEqual(ND(20040101).weekOfYear(),"1/2004") # thu
		self.assertEqual(ND(20030101).weekOfYear(),"1/2003") # wed
		self.assertEqual(ND(20020101).weekOfYear(),"1/2002") # tue
		self.assertEqual(ND(20010101).weekOfYear(),"1/2001") # mon
		self.assertEqual(ND(20010108).weekOfYear(),"2/2001") # mon
		self.assertEqual(ND(20000101).weekOfYear(),"52/1999") # sat
		self.assertEqual(ND(19990101).weekOfYear(),"53/1998") # fri
		self.assertEqual(ND(19950101).weekOfYear(),"52/1994") # sun
		
		self.assertEqual(ND(19950102).weekOfYear(),"1/1995") # mon
		self.assertEqual(ND(19990102).weekOfYear(),"53/1998") # sat
		self.assertEqual(ND(19990103).weekOfYear(),"53/1998") # sun
		self.assertEqual(ND(19990104).weekOfYear(),"1/1999") # mon
		
		self.assertEqual(ND(20040404).weekOfYear(),"14/2004") # sun
		self.assertEqual(ND(20040403).weekOfYear(),"14/2004") # sat
		self.assertEqual(ND(20040402).weekOfYear(),"14/2004") # fri
		self.assertEqual(ND(20040401).weekOfYear(),"14/2004") # thu
		self.assertEqual(ND(20040331).weekOfYear(),"14/2004") # wed
		self.assertEqual(ND(20040330).weekOfYear(),"14/2004") # tue
		self.assertEqual(ND(20040329).weekOfYear(),"14/2004") # mon
		self.assertEqual(ND(20040328).weekOfYear(),"13/2004") # sun
		

	def test02(self):
		day = ND(20040101)
		for i in range(350):
			day += 1
		self.assertEqual(day.dayOfYear(),351)
		
		# find monday of week containing 20040401
		day = ND(20040401)
		self.assertEqual(day.dayOfYear(),31+29+31+1)
		week = day.weekOfYear()
		self.assertEqual(week,"14/2004")
		while day.weekOfYear() == week:
			day -= 1
			
		day += 1
		self.assertEqual(str(day),'20040329')

		
		
if __name__ == '__main__':
	unittest.main()

