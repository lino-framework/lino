from lino.adamo import *
from babel import Languages

from addrbook import Persons, Cities
#from babel import Language
#from web import MemoMixin, MemoTreeMixin, TreeMixin

class Quotes(MemoTable):
	def init(self):
		MemoTable.init(self)
		self.id = Field(ROWID)
		self.author = Pointer(Authors)
		self.author.setDetail('quotesByAuthor')
		self.lang = Pointer(Languages)
		
		#self.pubRef = Field(STRING)
		#self.pub = Pointer("PUBLICATIONS")
		
	class Row(MemoTable.Row):
		def getLabel(self):
			return "[q"+str(self.id)+"]"

class Publications(MemoTreeTable):
	def init(self):
		MemoTreeTable.init(self)
		self.id = Field(ROWID)
		self.year = Field(INT)
		self.subtitle = Field(STRING)
		self.typeRef = Field(STRING)
		self.type = Pointer( PubTypes)
		self.author = Pointer(Authors)
		self.lang = Pointer(Languages)

class PubTypes(BabelTable):
	def init(self):
		self.id = Field(STRING)
		BabelTable.init(self)
		self.typeRefPrefix = Field(STRING)
		self.pubRefLabel = BabelField(STRING)
		

## 	def populate(self,area):
## 		q = area.query('id name typeRefPrefix pubRefLabel')
## 		q.appendRow("book",'Book','ISBN: ','page')
## 		q.appendRow("url",'Web Page','http:',None)
## 		q.appendRow("cd",'CompactDisc','cddb: ','track')
## 		q.appendRow("art",'Article','','page')
## 		q.appendRow("mag",'Magazine','','page')
## 		q.appendRow("sw",'Software','',None)


class Topics(TreeTable):
	def init(self):
		TreeTable.init(self)
		self.id = Field(ROWID)
		self.name = BabelField(STRING)
		#self.lang = Pointer(Languages)
		self.dewey = Field(STRING)
		self.cdu = Field(STRING)
		self.dmoz = Field(URL)
		self.wikipedia = Field(URL)
		self.url = BabelField(URL)
		self.addView('simple',"name url super children")
		
	class Row(TreeTable.Row):
		def getLabel(self):
			return self.name
	

class Authors(Persons):
	def init(self):
		self.id = Field(STRING)
		Persons.init(self)
		#self.birthDate = Field(DATE)
		#self.birthPlace = Pointer(City)
		#self.deathDate = Field(DATE)
		#self.deathPlace = Pointer(City)
	class Row(Persons.Row):
		pass


class AuthorEvents(BabelTable):
	"Birth, diplom, marriage, death..."
	def init(self):
		BabelTable.init(self)
		self.seq = Field(ROWID)
		self.type = Pointer(AuthorEventTypes)
		self.author = Pointer(Authors)
		self.date = Field(DATE)
		self.place = Pointer(Cities)
		#self.remark = Field(STRING)
		self.setPrimaryKey('author seq')
		
	class Row(BabelTable.Row):
		def getLabel(self):
			s = self.type.getLabel()
			if self.date is not None:
				s += " " + str(self.date)
			return s
		
class AuthorEventTypes(BabelTable):
	"Birth, diplom, marriage, death..."
	def init(self):
		BabelTable.init(self)
		self.id = Field(ROWID,\
						  doc="the internal" )
		#self.name = BabelField(STRING)
		

	class Row(BabelTable.Row):
		pass
