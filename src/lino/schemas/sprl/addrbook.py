from lino.adamo import *
#from lino.adamo.table import Table,LinkTable
#from lino.adamo.datatypes import *

# from lino.sprl.plugins import babel
from babel import Languages

class Contacts(Table):
	"abstract"
	def init(self):
		self.email = Field(EMAIL,
								 label="e-mail",
								 doc="Primary e-mail address")
		self.phone = Field(STRING,
								 doc="phone number")
		self.gsm = Field(STRING, label="mobile phone",
									  doc="mobile phone number")
		self.fax = Field(STRING, doc="fax number")
		self.website = Field(URL, doc="web site")

	class Row(Table.Row):
		def getLabel(self):
			return self.name
		
class Addresses(Table):
	""
	def init(self):
		self.nation = Pointer(Nations)
		self.city = Pointer(Cities)
		self.zip = Field(STRING)
		self.street = Field(STRING)
		self.house = Field(INT)
		self.box = Field(STRING)
		
	class Row(Table.Row):
		def after_city(self):
			if self.city is not None:
				self.nation = self.city.nation

class Organisations(Contacts,Addresses):
	"An Organisation is any named group of people."
	def init(self):
		self.id = Field(ROWID,\
						  doc="the internal id number")
		Contacts.init(self)
		Addresses.init(self)
		self.name = Field(STRING)

	class Row(Addresses.Row):
		pass

class Persons(Table): #(Contact,Address):
	"A Person describes a specific physical human."
	def init(self):
		self.id = Field(ROWID)
		self.name = Field(STRING)
		self.firstName = Field(STRING)
		
		# table.setFindColumns("name firstName")

		self.setColumnList("name firstName id")
		self.setOrderBy('name firstName')

	class Row(Table.Row):
		def getLabel(self):
			if self.firstName is None:
				return self.name
			return self.firstName+" "+self.name

		def validate(self):
			if (self.firstName is None) and (self.name is None):
				return "Either name or firstName must be specified"

	

class Users(Persons):
	"People who can access this database"
	def init(self):
		Persons.init(self)
		self.id = Field(STRING)

	class Row(Persons.Row):
		pass


class Partners(Contacts,Addresses):
	"""A Person or Organisation with whom I have business contacts.
	"""
	def init(self):
		self.name = Field(STRING)
		self.firstName = Field(STRING)
		Contacts.init(self)
		Addresses.init(self)
		self.id = Field(ROWID)
		self.type = Pointer(PartnerTypes)
		self.type.setDetail('partnersByType',orderBy='name firstName')
		self.title = Field(STRING)
		self.currency = Pointer(Currencies)
		self.logo = Field(LOGO)
		#self.org = Pointer(Organisation)
		#self.person = Pointer(Person)
		self.lang = Pointer(Languages)
		self.addView("simple","name firstName email phone gsm")
		
	class Row(Contacts.Row,Addresses.Row):
		def validate(self):
			if self.name is None:
				return "name must be specified"

		def getLabel(self):
			if self.firstName is None:
				return self.name
			return self.firstName+" "+self.name
	
## 	def on_org(self):
		
## 		"""Setting `org`of a Partner will also adapt the `name`.	 Some
## 		other fields are taken over from the Organisation only if they
## 		were None so far.	 """
		
## 		# print "on_org"
## 		if self.org is not None:
## 			self.name = self.org.getLabel() 
## 			#if self.phone is None:
## 			#	self.phone = self.org.phone 
## 	def on_person(self):
## 		# print "on_person"
## 		if self.person is not None:
## 			# row.name = row.person.fname + row.person.name
## 			self.name = self.person.getLabel() 
## 			#if self.phone is None:
## 			#	self.phone = self.person.phone 
				

class Currencies(BabelTable):
	
	def init(self):
		self.id = Field(STRING,width=3)
		BabelTable.init(self)
		
	class Row(BabelTable.Row):
		def __str__(self):
			return self.id
	
class PartnerTypes(BabelTable):
	
	def init(self):
		self.id = Field(STRING)
		BabelTable.init(self)
		
	def validatePartner(self,partner):
		# otherwise BabelTable.Row is not seen during schema startup
		pass
	
## 	def populate(self,area):
## 		q = area.query('id name')
## 		q.setUsedLangs('en')
## 		q.appendRow('c',('Customer',))
## 		q.appendRow('s',('Supplier',))
## 		q.appendRow('m',('Member',))
## 		q.appendRow('e',('Employee',))
## 		q.appendRow('d',('Sponsor',))

	class Row(BabelTable.Row):
		pass

## class PartnerType:
## 	def __init__(self,table):
## 		self.
## 	def validatePartner(self,partner):
## 		pass
	
	
	
	
class Nations(BabelTable):
	"""List of Nations (countries) .
	
	ISO 2-letter country codes."""
	def init(self):
		self.id = Field(STRING,width=2)
		BabelTable.init(self)
		self.area = Field(INT)
		self.population = Field(INT)
		self.curr = Field(STRING)
		self.isocode = Field(STRING)

	class Row(BabelTable.Row):
		def validate(self):
			if len(self.id) != 2:
				return "Nation.id must be 2 chars"
				#raise DataVeto("Nation.id must be 2 chars")
		

	
		
class Cities(Table):
	"""One record for each city.
	"""
	def init(self):
		self.id = Field(ROWID)
		self.nation = Pointer(Nations)
		self.nation.setDetail('cities',orderBy='name')
		
		self.name = Field(STRING)
		self.zipCode = Field(STRING)
		self.inhabitants = Field(INT)
		self.setPrimaryKey("nation id")
		# complex primary key used by test cases
		
	class Row(Table.Row):
		def getLabel(self):
			if self.nation is None:
				return self.name
			return self.name + " (%s)" % self.nation.id
		

	
class Org2Pers(LinkTable):
##		def __init__(self):
##			LinkTable.__init__(self,
##									 tables.ORGS,"persons",
##									 tables.PERSONS,"orgs")
	def init(self,table):
		self.note = Field(STRING)
		

		


