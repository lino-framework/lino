## Copyright Luc Saffre 2003-2004.

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
                      langs=None,
                      filename=None,
                      isTemporary=True
                      ):
    schema.startup()
    
    db = QuickDatabase( schema,
                        langs=langs,
                        filename=filename,
                        isTemporary=isTemporary
                        )
    db.createTables()
    
    sess = center.getCenter().createSession()
    
    sess.use(db=db,langs=langs)
    
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
           'INT', 'BOOL', 'ROWID', 'STRING',
           'DATE', 'TIME',
           'MEMO',
           'EMAIL', 'URL',
           'PRICE', 'AMOUNT', 
           'IMAGE', 'LOGO', 'PASSWORD']
