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
		self.addField('id',ROWID)
		self.addField('created',DATE)
		self.addField('modified',DATE)
		self.addPointer('author',Users)
		self.addPointer('lang',Languages)
		self.addField('match',STRING)
		
		#self.addField('pubRef',STRING)
		#table.addPointer("pub","PUBLICATIONS")

		#rpt = table.provideReport()
		#table.setColumnList('title abstract id created lang')
		#rpt.setLabel('Pages')

		self.addView('std',columnNames="title abstract")

	class Instance(MemoTreeTable.Instance):
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
		self.addField('seq',ROWID)
        
		self.setPrimaryKey(tuple())
