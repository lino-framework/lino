#coding: latin1
#----------------------------------------------------------------------
# $Id: babel.py,v 1.4 2004/06/18 12:23:58 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino.adamo import *

class Languages(Table):
	def init(self):
		self.id = Field(STRING,width=2)
		self.name = BabelField(STRING)
	
	class Row(Table.Row):
		def getLabel(self):
			return self.name

	
## 	def populate(self,area):
## 		q = area.query('id name_en')
## 		q.appendRow('en','English'	  )
## 		q.appendRow('de','German'	  )
## 		q.appendRow('et','Estonian'  )
## 		q.appendRow('fr','French'	  )
## 		q.appendRow('nl','Dutch'	  )
## 		#area.freeze()
