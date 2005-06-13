## Copyright 2003-2005 Luc Saffre 

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


from lino.adamo import *
from addrbook import Partners

class Journals(Table):
	def init(self):
		self.addField('id',STRING(width=3))
		self.addField('name',STRING).setMandatory()
		self.addField('tableName', STRING)
		
	class Instance(Table.Instance):
		def __str__(self):
			return self.name
		



class Years(Table):
	def init(self):
		self.addField('id',INT)
		self.addField('name',STRING)



class Documents(Table):
	def init(self):
		self.addField('seq',ROWID)
		self.addField('date',DATE)
		self.addField('closed',BOOL)

		self.addPointer('jnl',Journals).setDetail("documents")
		self.setPrimaryKey("jnl seq")

	class Instance(Table.Instance):
		def __str__(self):
			return self.jnl.id+"-"+str(self.seq)
		
##		def getNextId(self,jnl):
##			return self.getLastId(jnl.id) + 1
		
class FinancialDocuments(Documents):
	def init(self):
		Documents.init(self)
		self.addField('remark',STRING)
		
class BankStatements(FinancialDocuments):
	def init(self):
		FinancialDocuments.init(self)
		self.addField('balance1',AMOUNT)
		self.addField('balance2',AMOUNT)
		
class PartnerDocuments(Documents):
	def init(self):
		Documents.init(self)
		self.addField('remark',STRING)
		self.addPointer('partner',Partners)

		

