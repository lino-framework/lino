#coding: latin1

from lino.adamo import *

from babel import Languages
from addrbook import Persons, Partners
from web import Pages


class Events(Pages):
	def init(self):
		#MemoMixin.init(self,table)
		Pages.init(self)
		self.id = Field( ROWID)
		self.date = Field( DATE)
		self.time = Field( STRING)
		self.type = Pointer( EventTypes)
		self.type.setDetail("eventsByType")
		
		self.responsible = Pointer(Partners) 
		self.responsible.setDetail('eventsByResponsible')
		self.place = Pointer( Partners)
		self.place.setDetail('eventsByPlace')
		

		#self.setColumnList('date time place title abstract')
		self.setOrderBy("date time")

	class Row(Pages.Row):
		
		def getLabel(self):
			s = ''
			if self.title is None:
				s = self.type.title
			else:
				s = self.title
			s += " (" + str(self.date)
			if self.time is not None:
				s += ' ' + self.time + ' Uhr'
			s += ')'
			return s
	
class EventTypes(MemoTable):
	def init(self):
		MemoTable.init(self)
		self.id = Field(STRING)
		self.name = BabelField(STRING)
		#table.addDetail('eventsByType',Event)
		
	class Row(Table.Row):
		def getLabel(self):
			return self.title
		
