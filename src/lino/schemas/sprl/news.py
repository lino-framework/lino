"""
"""

# from lino import adamo
from lino.adamo import *

from babel import Languages
from web import Pages
from addrbook import Users
from projects import Projects

class News(MemoTable):
	
	def init(self):
		MemoTable.init(self)
		self.id = Field(ROWID)
		self.date = Field(DATE)
		self.newsgroup = Pointer(Newsgroups)
		self.newsgroup.setDetail('newsByGroup',
										  #label="News by Group",
										  orderBy='date')
		self.author = Pointer(Users)
		self.author.setDetail('newsByAuthor')
		self.lang = Pointer(Languages)
		self.project = Pointer(Projects)
		self.page = Pointer(Pages)

		#table.setColumnList('date title newsgroup abstract id lang')
		self.setOrderBy("date")
		
	class Row(MemoTable.Row):
		def getLabel(self):
			s = str(self.date)
			if self.newsgroup is not None:
				s += ' (%s)' % self.newsgroup.getLabel()
			if self.title:
				s += " " + self.title
			return s
	
class Newsgroups(Table):
	def init(self):
		self.id = Field(STRING)
		self.name = Field(STRING)
		
	class Row(Table.Row):
		def getLabel(self):
			return self.name
		
## 	def asPage(self,renderer):
## 		body = ''
## 		newsByGroup = NEWS
