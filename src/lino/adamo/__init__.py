"""
adamo : Abstract Data Model

"""

from lino import __version__
# __version__ = "0.1.0"

import __builtin__
import sys

from table import Table, LinkTable,\
	  MemoTable, TreeTable, MemoTreeTable,\
	  BabelTable
from forms import FormTemplate
from widgets import Menu, Command
from datatypes import *
from rowattrs import Field, Pointer, BabelField, Vurt, Match#, Button
from schema import Schema, SchemaPlugin
from context import ConsoleSession
from datasource import DataRow
from database import QuickDatabase as quickdb

def _(s):
   return s

__builtin__.__dict__['_'] = _

 


__all__ = ['Table','LinkTable',
			  'TreeTable', 'MemoTable', 'MemoTreeTable',
			  'BabelTable',
			  'Field','Pointer','BabelField','Vurt','Match',#'Button',
			  'DataVeto','InvalidRequestError',
			  'DataRow',
			  'FormTemplate','Menu','Command',
			  'Schema','SchemaPlugin',
			  'ConsoleSession',
			  'quickdb',
			  'INT', 'BOOL', 'ROWID', 'STRING', 'DATE', 'MEMO',
			  'EMAIL', 'URL',
			  'PRICE', 'AMOUNT', 
			  'IMAGE', 'LOGO', 'PASSWORD']
