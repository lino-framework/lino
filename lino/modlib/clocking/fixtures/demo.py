# -*- coding: UTF-8 -*-
"""

"""
from __future__ import unicode_literals
from __future__ import print_function

import datetime

from lino.api import rt, dd
from lino.utils import Cycler

from lino.modlib.cal.utils import DurationUnits


def objects():
    SessionType = rt.modules.clocking.SessionType
    Session = rt.modules.clocking.Session
    Ticket = rt.modules.tickets.Ticket
    User = rt.modules.users.User
    UserProfiles = rt.modules.users.UserProfiles
    devs = (UserProfiles.developer, UserProfiles.senior)
    workers = User.objects.filter(profile__in=devs)
    WORKERS = Cycler(workers)
    TYPES = Cycler(SessionType.objects.all())
    TICKETS = Cycler(Ticket.objects.all())
    DURATIONS = Cycler([5, 12, 13, 20, 10, 20, 20, 3, 6, 17, 23])

    for t in Ticket.objects.all():
        t.assigned_to = WORKERS.pop()
        yield t

    for u in workers:

        ts = datetime.datetime.combine(
            dd.demo_date(), datetime.time(9, 0, 0))
    
        TICKETS = Cycler(Ticket.objects.filter(assigned_to=u))

        for i in range(20):
            obj = Session(
                ticket=TICKETS.pop(), session_type=TYPES.pop(), user=u)
            obj.set_datetime('start', ts)
            ts = DurationUnits.minutes.add_duration(ts, DURATIONS.pop())
            obj.set_datetime('end', ts)
            yield obj

    ServiceReport = rt.modules.clocking.ServiceReport
    Site = rt.modules.tickets.Site
    welket = Site.objects.get(name="welket")
    yield ServiceReport(
        start_date=dd.today(-90), interesting_for=welket)
