# coding: latin1

"""
Logical columns (row attributes) versus physical columns (atoms)

"""
import types

from lino.misc.tsttools import TestCase
from lino.schemas.sprl import demo

class Case(TestCase):
	"""
	selecting "WHERE x is NULL"
	"""

	def setUp(self):
		
		self.sess = demo.beginSession()

	def tearDown(self):
		self.sess.shutdown()


	def test01(self):
		PROJECTS = self.sess.tables.PROJECTS
		ds = PROJECTS.query("id super.id title")
		self.assertEqual(len(ds),10)
		s = ""
		for p in ds:
			s+= "\t".join([str(cell.getValue()) for cell in p]) + "\n"
		#print s
		self.assertEqual(s,"""\
1	None	Project 1
2	None	Project 2
3	None	Project 3
4	1	Project 1.1
5	1	Project 1.2
6	1	Project 1.3
7	6	Project 1.3.1
8	6	Project 1.3.2
9	8	Project 1.3.2.1
10	8	Project 1.3.2.2
""")		
		
		"""
		The Python value None is principally translated as NULL to SQL.

		For example, specifying super=None will select only the
		top-level projects (whose super is NULL): """
		
		ds = PROJECTS.query("id title", super=None)
		self.assertEqual(len(ds),3)
		s = ""
		for p in ds:
			s+= "\t".join([str(cell.getValue()) for cell in p]) + "\n"
		#print s
		self.assertEqual(s,"""\
1	Project 1
2	Project 2
3	Project 3
""")


		"""

		Samples are sticky properties: once set, the get inherited by
		all children.  To clear a sample, you must explicitly set it to
		Datasource.ANY_VALUE.
		
		Example: you want to use the ds from above as parent for a new
		ds because you want to inherit columnNames. But now you want to
		see them all, not only the top-level projects.  So you must
		clear the "super=None" condition.

		"""
		
		ds = ds.query(orderBy="title",super=ds.ANY_VALUE)
		self.assertEqual(len(ds),10)

		
		"""
		Calling
		http://localhost:8080/lino/db/PROJECTS?v=std
		must show only the projects with super=None
		"""

		ds = PROJECTS.query(viewName="std")
		self.assertEqual(len(ds),3)

		

		try:
			ds = PROJECTS.query(viewName="nonExistingViewName")
			self.fail("failed to raise exception for bad viewName")
		except KeyError:
			pass
		
		



if __name__ == '__main__':
	import unittest
	unittest.main()

