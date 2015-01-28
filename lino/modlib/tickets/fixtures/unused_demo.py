# -*- coding: UTF-8 -*-
# Copyright 2011-2012 Luc Saffre
# License: BSD (see file COPYING for details)

from django.conf import settings

from lino.core.utils import resolve_model
from lino.utils.instantiator import Instantiator, i2d
from lino.utils import dblogger
#from lino import reports
#contacts = reports.get_app('contacts')


def objects():
    # ~ dblogger.info("Installing contacts demo fixture") # use --verbosity=2
    User = resolve_model(settings.SITE.user_model)
    Company = resolve_model("contacts.Company")
    Session = resolve_model('tickets.Session')
    #~ u = User.objects.get(username='root')
    u = User.objects.all()[0]

    rumma = Company.objects.get(name=u'Rumma & Ko OÜ')

    project = Instantiator('tickets.Project', "name", user=u).build
    yield project("TIM")
    lino = project("Lino")
    yield lino
    presto = project("Presto", parent=lino)
    yield presto
    cbss = project("CBSS connection", parent=lino)
    yield cbss

    milestone = Instantiator(
        'tickets.Milestone', "label reached", project=lino).build
    yield milestone('1.4.3', i2d(20120328))
    yield milestone('1.4.5', i2d(20120716))
    yield milestone('1.4.7', i2d(20120717))
    yield milestone('1.4.8', i2d(20120722))
    yield milestone('1.4.9', None)

    ticket = Instantiator('tickets.Ticket', "summary",
                          user=u, project=presto, partner=rumma).build
    presto_proto = ticket(summary="write a first prototype", project=presto)
    yield presto_proto

    #~ session = Instantiator('tickets.Session',"description",user=u,ticket=t).build
    yield Session(date=i2d(20111113),
                  user=u, ticket=presto_proto, start_time='21:45', end_time='23:28',
        description="""\
Created new module (tested in `lino_local.luc`).
Tried first with EventsByTicket instead of Comments,
but Comments are not usually planned.""")
    yield Session(date=i2d(20120603),
                  user=u, ticket=presto_proto, start_time='21:45', end_time='23:28',
        description="""\
replaced Comment by Session.
""")

    yield Session(date=i2d(20120604),
                  user=u, ticket=presto_proto, start_time='08:10', end_time='10:30',
        description="""\
labels, titles, tidy up, EntriesBySession.
""")

    yield Session(date=i2d(20120629),
                  user=u, ticket=presto_proto, start_time='00:05', end_time='01:15',
        description="""\
ProjectsByPartner
""")

    yield Session(date=i2d(20120727),
                  user=u, ticket=presto_proto, start_time='02:30', end_time='03:15',
        description="""\
TicketsByPartner
""")
