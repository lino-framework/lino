"""
adamo : Abstract Database Model

"""

from lino import __version__
# __version__ = "0.1.0"

import __builtin__
import sys

from table import Table, LinkTable,\
	  MemoTable, TreeTable, MemoTreeTable,\
	  BabelTable
from datatypes import *
from rowattrs import Field, Pointer, BabelField
from schema import Schema
from datasource import DataRow
from database import QuickDatabase as quickdb

def _(s):
   return s

__builtin__.__dict__['_'] = _

 


__all__ = ['Table','LinkTable',
			  'TreeTable', 'MemoTable', 'MemoTreeTable',
			  'BabelTable',
			  'Field','Pointer','BabelField',
			  'DataVeto','DataRow',
			  'Schema','quickdb',
			  'INT', 'BOOL', 'ROWID', 'STRING', 'DATE', 'MEMO',
			  'EMAIL', 'URL',
			  'PRICE', 'AMOUNT', 
			  'IMAGE', 'LOGO']
