# coding: latin1

""" 20040206 : bug fixed

problem when accessing data that was already in the database.

In the following test, p[2] returned the same row as the previous p[1]


"""
import unittest
#from lino.adamo.dbds.sqlite_dbd import Connection
from lino.schemas.sprl import demo #.sprl import Schema
#from lino.adamo.ui import UI

class Case(unittest.TestCase):

	def test01(self):
		"Accessing data that has not been inserted using adamo"
		db = demo.getDemoDB(populator=None)
		
## 		ui = UI(verbose=False)
## 		schema = Schema()
## 		schema.startup(ui)
	
## 		conn = Connection("tmp.db",isTemporary=True)
		
## 		db = ui.addDatabase('demo',conn,schema,label="Lino Demo Database")

## 		# db.connect(conn)
## 		db.createTables()
		
		db.connection.sql_exec("""
		INSERT INTO PARTNERS (id,name)
		       VALUES (1, "Luc");
		""")

		db.connection.sql_exec("""
		INSERT INTO PARTNERS (id,name)
		       VALUES (2, "Ly");
		""")

		db.installto(globals())

		#ctx = db.beginContext()
		#p = ctx.PARTNERS

		#self.assertEqual(len(p._cachedRows),0)
		luc = PARTNERS.peek(1)
		self.assertEqual(luc.id,1)
		self.assertEqual(luc.name,"Luc")
		ly = PARTNERS.peek(2)
		self.assertEqual(ly.id,2)
		self.assertEqual(ly.name,"Ly")

		self.failIf(luc.isDirty())
		self.failIf(ly.isDirty())
		
		#self.failUnless(luc.isComplete())
		#self.failUnless(ly.isComplete())

		#print luc.getValues()
		#print ly.getValues()
		
		#self.assertNotEqual(luc,ly)
		
		#self.assertEqual(p[1].name,'Luc')

		# the following tests failed:
		# self.assertEqual(p[2].id,2)
		# self.assertEqual(p[2].name,'Ly')

		db.shutdown()

	def test02(self):
		d = {}
		id1 = (1,)
		id2 = (2,)
		s1 = "Luc"
		s2 = "Ly"
		d[id1] = s1
		d[id2] = s2
		
		self.assertEqual(d[id1],'Luc')
		self.assertEqual(d[id2],'Ly')

if __name__ == '__main__':
	unittest.main()

