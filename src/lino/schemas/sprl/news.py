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

		#self.writeParagraph = Vurt(self.Instance.writeParagraph,MEMO)

		#table.setColumnList('date title newsgroup abstract id lang')
		self.setOrderBy("date")
		self.addView("simple","date title abstract",
						 orderBy="date")
		self.addView("list","date writeParagraph",
						 orderBy="date")
		
	class Instance(MemoTable.Instance):
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
		
	class Instance(Table.Instance):
		def getLabel(self):
			return self.name
		
## 	def asPage(self,renderer):
## 		body = ''
## 		newsByGroup = NEWS
