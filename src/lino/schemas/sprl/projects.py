from lino.adamo import *
from addrbook import Users, Partners
#from web import MemoMixin, MemoTreeMixin


class Projects(MemoTreeTable):
	
	def init(self):
		MemoTreeTable.init(self)
		self.id = Field(ROWID)
		self.date = Field(DATE)
		self.stopDate = Field(DATE)

		self.responsible = Pointer(Users)
		self.responsible.setDetail("projects")
		self.sponsor = Pointer( Partners) #,"projects")
		self.status = Pointer( ProjectStati)
		self.status.setDetail("projects")
		
		#from sdk import Version
		#self.version = Pointer(Version,"projects")

		self.addView("std",
						 columnNames="title abstract status",
						 label="Top-level projects",
						 super=None)

	class Row(MemoTreeTable.Row):
		pass


class ProjectStati(BabelTable):
	"list of codes used to formulate how far a project is"
	def init(self):
		BabelTable.init(self)
		self.id = Field(STRING)
		#self.name = BabelField(STRING)

## 	def populate(self,area):
## 		q = area.query('id title')
## 		q.appendRow('T','to do')
## 		q.appendRow('D','done');
## 		q.appendRow('W','waiting');
## 		q.appendRow('A','abandoned');
## 		q.appendRow('S','sleeping');		
