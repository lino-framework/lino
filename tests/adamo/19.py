# coding: latin1
"""
20040513



"""
import unittest
import types

from lino.adamo import *
from lino import adamo

## from lino.adamo.datatypes import \
## 	  DataVeto, StartupDelay, \
## 	  STRING, ROWID, INT, EMAIL

## from lino.adamo import schema
## from lino.adamo.schema import quickdb

from lino.adamo.paramset import ParamOwner

from lino.adamo.rowattrs import Field, BabelField, Pointer, \
	  RowAttribute

from lino.adamo.table import Table


class Nations(Table):
	def init(self):
		self.id = Field(STRING,width=2)
		self.name = BabelField(STRING)
		self.area = Field(INT)
		self.population = Field(INT)
		self.curr = Field(STRING)
		self.isocode = Field(STRING)

## 	def validateRow(self,row):
## 		if len(row.id) != 2:
## 			return "id must be 2 chars"
## 			#raise DataVeto("Nation.id must be 2 chars")
		
## 	def getRowLabel(self,row):
## 		return row.name_en
		
class Cities(Table):
	
	def init(self):
		self.id = Field(ROWID)
		self.nation = Pointer(Nations)
		self.nation.setDetail('cities',orderBy='name')
		self.name = Field(STRING)
		self.zipCode = Field(STRING)
		self.inhabitants = Field(INT)
		self.setPrimaryKey("nation id")
		
	class Instance(Table.Instance):
		def getLabel(self):		
			if self.nation is None:
				return self.name
			return self.name + " (%s)" % self.nation.id
		

class Contacts:
	def init(self):
		self.email = Field(EMAIL)
		self.phone = Field(STRING)

class Addresses:
	def init(self):
		self.nation = Pointer(Nations)
		self.city = Pointer(Cities)
		self.street = Field(STRING)

	def after_city(self,row):
		if row.city is not None:
			row.nation = row.city.nation

class Organisations(Table,Contacts,Addresses):
	"An Organisation is any named group of people."
	def init(self):
		self.id = Field(ROWID, doc="the internal id number")
		self.name = Field(STRING)
		Contacts.init(self)
		Addresses.init(self)


class MyPlugin(SchemaPlugin):
	
	def defineTables(self,schema):
		schema.addTable(Nations())
		schema.addTable(Cities())
		schema.addTable(Organisations())
		


class Case(unittest.TestCase):
	
	def test01(self):

		schema = Schema()
		schema.addPlugin(MyPlugin())

		sess = adamo.beginQuickSession(schema,
												 langs='en de fr',
												 isTemporary=True
												 )

		
		
		ds = sess.tables.Nations.query()

		sess.setBabelLangs('en')
		be = ds.appendRow(id="be", name="Belgium")
		de = ds.appendRow(id="de", name="Germany")

		be.lock()
		de.lock()

		
		sess.setBabelLangs('de')
		be.name = "Belgien"
		de.name = "Deutschland"
		
		sess.setBabelLangs('fr')
		be.name = "Belgique"
		de.name = "Allemagne"

		be.unlock()
		de.unlock()
		
		
		#print ctx._db._connection.stopDump()

## 		be = ds.appendRow(id="be",
## 								name=("Belgium","Belgien","Belgique"))
## 		de = ds.appendRow(id="de",
## 								name=("Germany","Deutschland","Allemagne"))
		
		#print be._values['name']
		#ctx._db._connection.startDump()
		be = sess.tables.Nations.peek('be')
		#print ctx._db._connection.stopDump()
		#print be._values['name']
		
		sess.tables.Cities.appendRow(nation=be,name="Eupen")
		
		sess.setBabelLangs('de')
		self.assertEqual(be.name,'Belgien')
		
		sess.setBabelLangs('fr')
		self.assertEqual(be.name,'Belgique')
		
		sess.setBabelLangs('en')
		self.assertEqual(be.name,'Belgium')
		
		sess.setBabelLangs('en de')
		self.assertEqual(be.name,['Belgium','Belgien'])
		
		sess.shutdown()

		

		
if __name__ == '__main__':
	unittest.main()

