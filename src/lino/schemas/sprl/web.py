#----------------------------------------------------------------------
# $Id: web.py,v 1.11 2004/06/12 03:06:52 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino.adamo import *

from babel import Languages
from addrbook import Users

		
#	def getChildren(self):
#		return self._area.instances( orderBy='seq',
#											  samples={'super':self})

class Pages(MemoTreeTable):
	def init(self):
		MemoTreeTable.init(self)
		self.id = Field(ROWID)
		self.created = Field(DATE)
		self.modified = Field(DATE)
		self.author = Pointer(Users)
		self.lang = Pointer(Languages)
		self.match = Field(STRING)
		
		#self.pubRef = Field(STRING)
		#table.addPointer("pub","PUBLICATIONS")

		#rpt = table.provideReport()
		#table.setColumnList('title abstract id created lang')
		#rpt.setLabel('Pages')

		self.addView('std',columnNames="title abstract")

	class Row(MemoTreeTable.Row):
		pass
	
## 	def validate(self):
## 		if self.match is not None:
## 			pass


## 	def __html__(self,renderer,request,fmt):
## 		if fmt == renderer.FMT_PAGE:
			
## 			#body += "<p>"
## 			#body += memo2html(row.body)

## 			body += "<ul>"
## 			for child in self.children(orderBy="seq").instances():
				
## 				body += '<li>' + renderer.renderLink(
## 					url=renderer.rowUrl(child),
## 					label=child.getLabel())
## 				body += renderer.memo2html(child.abstract)
## 				body += "</li>"
## 			body += "</ul>"
## 			return body
		
## 		return renderer.renderLink(url=renderer.rowUrl(self),
## 											label=self.getLabel())
		
			
class Page2Page(Table):
	def init(self):
		self.seq = Field(ROWID)
		self.setPrimaryKey(tuple())
