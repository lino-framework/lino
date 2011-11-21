## Copyright 2003-2006 Luc Saffre

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

"""
adamo : Abstract Data Model

"""

from lino import __version__
#__version__ = "0.0.1 pre"

import __builtin__
import sys

## from lino.adamo.table import Table, LinkTable,\
##      MemoTable, TreeTable, MemoTreeTable,\
##      BabelTable

#from lino.adamo.forms import Form
#from widgets import Menu, Command
from lino.adamo.datatypes import *
from lino.adamo.exceptions import *
#from lino.adamo.rowattrs import Field, Pointer, BabelField, Vurt
#, Match#, Button
#from lino.adamo.schema import Schema, SchemaPlugin
#from lino.adamo.store import Populator
#from session import ConsoleSession
#from session import Application
#from lino.adamo.row import DataRow
#from database import QuickDatabase 
#from center import Center

## def _(s):
##    return s

## __builtin__.__dict__['_'] = _


## def beginQuickSession(schema,*args,**kw):
    
##     print """adamo.__init__.py: use schema.quickStart() instead of
##     deprecated adamo.beginQuickSession(schema)"""
    
##     schema.quickStartup(*args,**kw)
    
## def beginQuickSession(schema,
##                       langs=None, filename=None,
##                       **kw):
    
##     schema.initialize()
##     db = QuickDatabase(schema, langs=langs, filename=filename)
##     return center.startup(**kw)

##     sess = center.startup(**kw)
##     sess.use(db=db,langs=langs)
##     return sess



__all__ = [#'Table','LinkTable',
           #'TreeTable', 'MemoTable', 'MemoTreeTable',
           #'BabelTable',
           #'Field','Pointer','BabelField','Vurt',
           #'Match',#'Button',
           'DataVeto','InvalidRequestError',
           #'DataRow',
           #'Form',
           #'Menu','Command',
           #'Schema','SchemaPlugin',
           #'Populator',
           #'ConsoleSession',
           #'Application',
           #'quickdb',
##            'INT', 'BOOL', 'ROWID', 'STRING',
##            'DATE', 'TIME', 'DURATION',
##            'MEMO',
##            'EMAIL', 'URL',
##            'PRICE', 'AMOUNT', 
##            'IMAGE', 'LOGO', 'PASSWORD'
           ]
