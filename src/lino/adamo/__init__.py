"""
adamo : Abstract Data Model

"""

#from lino import __version__
__version__ = "0.0.1 pre"

import __builtin__
import sys

from table import Table, LinkTable,\
	  MemoTable, TreeTable, MemoTreeTable,\
	  BabelTable
from forms import Form
#from widgets import Menu, Command
from datatypes import *
from rowattrs import Field, Pointer, BabelField, Vurt #, Match#, Button
from schema import Schema, SchemaPlugin
#from session import ConsoleSession
#from session import Application
from datasource import DataRow
from database import QuickDatabase 
import center

def _(s):
   return s

__builtin__.__dict__['_'] = _


def beginQuickSession(schema,
							 populator=None,
							 langs=None,
							 isTemporary=True,
							 #verbose=None
							 ):
## 	if verbose is not None:
## 		start(verbose=verbose)
		
## 	ctr = center()
## 	if app is None:
## 		app =	Application(verbose=verbose)
## 	else:
## 		assert verbose is False
		
	schema.startup()
	
	db = QuickDatabase( schema,
							  langs=langs,
							  isTemporary=isTemporary
							  )
	db.createTables()
	
	sess = center.getCenter().createSession()
	
	sess.use(db=db,langs=langs)
	
	if populator:
		populator(sess)
		
	return sess


 


__all__ = ['Table','LinkTable',
			  'TreeTable', 'MemoTable', 'MemoTreeTable',
			  'BabelTable',
			  'Field','Pointer','BabelField','Vurt',
			  #'Match',#'Button',
			  'DataVeto','InvalidRequestError',
			  'DataRow',
			  'Form',
			  #'Menu','Command',
			  'Schema','SchemaPlugin',
			  #'ConsoleSession',
			  #'Application',
			  #'quickdb',
			  'INT', 'BOOL', 'ROWID', 'STRING', 'DATE', 'MEMO',
			  'EMAIL', 'URL',
			  'PRICE', 'AMOUNT', 
			  'IMAGE', 'LOGO', 'PASSWORD']
