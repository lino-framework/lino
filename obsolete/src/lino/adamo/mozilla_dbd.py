#----------------------------------------------------------------------
# $Id: mozilla_dbd.py,v 1.1 2004/06/12 03:13:27 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import types
import warnings 

from lino.adamo import 
from datatypes import *
from rowattrs import Field, Pointer #, Detail

from connection import Connection


class MailboxSchema(Schema):
	def defineTables(self):
		self.addTable(Folders())
		self.addTable(Addresses())
		self.addTable(Messages())
		self.addTable( babel.Languages(), "LANGS")


class MailboxConnection(Connection):

