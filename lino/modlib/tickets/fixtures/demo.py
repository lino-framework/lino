# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
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

from lino.core.modeltools import resolve_model
from lino.utils.instantiator import Instantiator, i2d
from lino.utils import dblogger
#from lino import reports
#contacts = reports.get_app('contacts')


def objects():
    #~ dblogger.info("Installing contacts demo fixture") # use --verbosity=2
    User = resolve_model(settings.LINO.user_model)
    Session = resolve_model('tickets.Session')
    u = User.objects.get(username='root')
    
    project = Instantiator('tickets.Project',"name",user=u).build
    yield project("TIM")
    lino = project("Lino")
    yield lino
    presto = project("Presto",parent=lino)
    yield presto 
    cbss = project("CBSS connection",parent=lino)
    yield cbss 
    
    ticket = Instantiator('tickets.Ticket',"summary",user=u,project=presto).build
    t = ticket(summary="write a first prototype",project=presto)
    yield t

    #~ session = Instantiator('tickets.Session',"description",user=u,ticket=t).build
    yield Session(date=i2d(20111113),
        user=u,ticket=t,start_time='21:45',end_time='23:28',
        description="""\
Created new module (tested in `lino_local.luc`).
Tried first with EventsByTicket instead of Comments,
but Comments are not usually planned.""")
    yield Session(date=i2d(20120603),
        user=u,ticket=t,start_time='21:45',end_time='23:28',
        description="""\
replaced Comment by Session.
""")

    yield Session(date=i2d(20120604),
        user=u,ticket=t,start_time='08:10',end_time='10:30',
        description="""\
labels, titles, tidy up, EntriesBySession.
""")
