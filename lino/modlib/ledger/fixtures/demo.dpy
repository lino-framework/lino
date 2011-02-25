# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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
from datetime import date
from dateutil import parser as dateparser
from lino.modlib.ledger import models as ledger
#from lino.apps.journals import models as journals
from lino.modlib.ledger.fixtures import be
from lino.utils.instantiator import Instantiator, i2d

#journal = Instantiator(journals.Journal,"id name")
#account = Instantiator(ledger.Account,"name").build
account = Instantiator(ledger.Account,"match name").build

def objects():
    for ln in be.PCMN.splitlines():
        a = ln.split(None,1)
        if len(a) == 2:
            yield account(*a)
    
