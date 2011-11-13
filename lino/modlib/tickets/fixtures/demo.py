# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
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

from django.conf import settings

from lino.tools import resolve_model
from lino.utils.instantiator import Instantiator
from lino.utils.babel import default_language
from lino.utils import dblogger
#from lino import reports
#contacts = reports.get_app('contacts')


def objects():
    #~ dblogger.info("Installing contacts demo fixture") # use --verbosity=2
    User = resolve_model(settings.LINO.user_model)
    u = User.objects.get(username='root')
    
    project = Instantiator('tickets.Project',"name",user=u).build
    yield project("TIM")
    p = project("Lino")
    yield p
    
    ticket = Instantiator('tickets.Ticket',"summary",user=u,project=p).build
    yield ticket("BCSS connection")
    t = ticket("new module lino.modlib.tickets")
    yield t

    comment = Instantiator('tickets.Comment',"description",user=u,ticket=t).build
    yield comment("""\
Created new module (tested in `lino_local.luc`).
Tried first with EventsByTicket instead of Comments,
but Comments are not usually planned.""")
