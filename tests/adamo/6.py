#coding: latin1
   
import sys

from StringIO import StringIO

from lino.misc.tsttools import TestCase

from lino.examples import pizzeria,pizzeria2

def catch_output(f,*args,**kw):
	out = sys.stdout
	sys.stdout = StringIO()
	f(*args,**kw)
	r = sys.stdout.getvalue()
	sys.stdout = out
	return r



class Case(TestCase):
	def test01(self):
		"do the pizzeria examples work?"
		
		self.assertEquivalent(catch_output(pizzeria.main),"""\
Henri must pay 12 EUR
James must pay 53 EUR
""")
		self.assertEquivalent(catch_output(pizzeria2.main),"""\
Order #: 3
Date: 20040318
Customer: Bernard
----------------------------------------
Pizza Margerita        1     6
bring home             1     1
----------------------------------------
Total:  7
""")


	def test_voc(self):
		return None # the voc example is sleeping
		from lino.examples import voc
		voc.main()
		

if __name__ == '__main__':
	from unittest import main
	main()

