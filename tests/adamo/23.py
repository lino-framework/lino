# coding: latin1

"""
Logical columns (row attributes) versus physical columns (atoms)

"""
import types

from lino.misc.tsttools import TestCase
from lino.schemas.sprl import demo

class Case(TestCase):

	def setUp(self):
		
		self.db = demo.getDemoDB()
		self.db.installto(globals()) 

	def tearDown(self):
		self.db.shutdown()


	def test01(self):
		"create an invoice"

		
		"""get the partner # 1 and Journal."""
		p = PARTNERS.peek(1)
		self.assertEqual(p.getLabel(),"Luc Saffre")

		jnl = JOURNALS.peek("OUT")
		self.assertEqual(jnl.id,"OUT")

		"create a query"
		
		invoices = INVOICES.query("jnl date remark",
										  partner=p)
		#invoices.setSamples(partner=p)
		#csr = invoices.executeSelect()
		#count = csr.rowcount
		count = len(invoices)
		

		self.assertEqual(count,0)

		# create a new invoice :
		i = invoices.appendRow(jnl,"2003-08-16","test")
		
		"""
		The `seq` field of INVOICES is an auto-incrementing integer.
		"""
		self.assertEqual(i.seq,2)

		
		#i.commit()

		# self.db.commit()

		"""the following should be equivalent :
		i = p.invoices.appendRow()
		"""


		""" len(p.invoices) is increased because an invoice for this
		partner has been created:"""

		"""create two rows in this invoice :"""

		#lines = INVOICELINES.query("line product qty",invoice=i)
		#lines.setSamples(invoice=i)

		lines = i.lines.query("line product qty")

		lines.appendRow(1,PRODUCTS.peek(3), 2) # price is 12
		lines.appendRow(2,PRODUCTS.peek(16), 3) # price is 56

		# INVOICELINES.commit()

		l = []
		for line in lines:
			l.append(str(line.product.name))
		s = " ".join(l)
		self.assertEqual(s,"Chair Table")
			
		# register() the invoice :
		i.close()
		
		self.assertEqual(i.amount, 2*12 + 3*56 )

##			# get a cursor on BOOKINGS :
##			q = BOOKINGS.query("invoice")

##			# we want only the bookings for one invoice
##			q.setSlice(q.invoice,i)

##			"""first invocation of len() will silently execute a query to
##			find out the number of rows. There must be 2 rows"""

##			# bc.executeCount()

##			self.assertEqual(len(q),2)



if __name__ == '__main__':
	import unittest
	unittest.main()

