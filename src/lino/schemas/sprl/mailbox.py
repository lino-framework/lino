#----------------------------------------------------------------------
# $Id: mailbox.py,v 1.1 2004/06/12 03:13:27 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino.adamo import *

from babel import Languages
from addrbook import Users
#from web import TreeMixin

class Folders(TreeTable):
	def init(self):
		TreeTable.init(self)
		self.name = Field(STRING)


class Addresses(Table):
	def init(self):
		self.name = Field(STRING)
		self.email = Field(EMAIL)
	
class Messages(Table):
	def init(self):
		self.subject = Field(STRING)
		self.recipient = Pointer(Recipients))
		
		
