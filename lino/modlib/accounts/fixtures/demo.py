# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

import time
#~ from datetime import date
#~ from dateutil import parser as dateparser
#~ from lino.modlib.ledger import models as ledger
#from lino.apps.journals import models as journals
from lino.utils.instantiator import Instantiator, i2d
from lino.utils.babel import babel_values
from lino.modlib.accounts.utils import AccountTypes

from lino import dd
accounts = dd.resolve_app('accounts')

#journal = Instantiator(journals.Journal,"id name")
#account = Instantiator(ledger.Account,"name").build

def objects():
    from lino.modlib.accounts.fixtures import mini
    yield mini.objects()
    
        
        
