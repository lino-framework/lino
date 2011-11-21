## Copyright 2005-2006 Luc Saffre 

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

raise "moved to keeper_tables.py"

import os

import keeper_tables as tables
#from lino.apps.keeper.tables import TABLES
#from lino.apps.keeper.tables import *
from lino.adamo.ddl import STRING, BOOL
from lino.adamo.dbreports import DataReport
from lino.forms.forms import ReportForm, DbMainForm
from lino.forms.gui import DbApplication



## if __name__ == '__main__':
##     from lino.forms import gui
##     app=Keeper()
##     sess=app.quickStartup()
##     sess.populate(TestPopulator())
##     gui.run(sess)
