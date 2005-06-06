#coding: latin1

from lino.adamo.ddl import *

from lino.schemas.sprl.addrbook import Partners
from web import Pages


class Events(Pages):
	def init(self):
		#MemoMixin.init(self,table)
		Pages.init(self)
		self.addField('id', ROWID)
		self.addField('date', DATE)
		self.addField('time', STRING)
		self.addPointer('type', EventTypes).setDetail("eventsByType")
		
		self.addPointer('responsible',Partners).setDetail(
            'eventsByResponsible')
		self.addPointer('place',Partners).setDetail('eventsByPlace')
		

		#self.setColumnList('date time place title abstract')
		self.setOrderBy("date time")

	class Instance(Pages.Instance):
		
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
		self.addField('id',STRING)
		self.addBabelField('name',STRING)
		#table.addDetail('eventsByType',Event)
		
	class Instance(Table.Instance):
		def getLabel(self):
			return self.title
		
