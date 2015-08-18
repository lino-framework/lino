# -*- coding: UTF-8 -*-
"""

"""
from __future__ import unicode_literals
from __future__ import print_function

import datetime

from lino.api import rt, dd
from lino.utils import Cycler

from lino.modlib.cal.utils import DurationUnits
from lino.modlib.tickets.roles import Worker
from lino.utils.quantities import Duration


def objects():
    SessionType = rt.modules.clocking.SessionType
    Session = rt.modules.clocking.Session
    Ticket = rt.modules.tickets.Ticket
    # TicketStates = rt.modules.tickets.TicketStates
    User = rt.modules.users.User
    UserProfiles = rt.modules.users.UserProfiles
    # devs = (UserProfiles.developer, UserProfiles.senior)
    devs = [p for p in UserProfiles.items() if p.has_required_roles([Worker])]
    workers = User.objects.filter(profile__in=devs)
    WORKERS = Cycler(workers)
    TYPES = Cycler(SessionType.objects.all())
    TICKETS = Cycler(Ticket.objects.all())
    DURATIONS = Cycler([12, 138, 90, 10, 122, 209, 37, 62, 179, 233, 5])

    # every third ticket is unassigned and thus listed in PublicTickets
    for i, t in enumerate(Ticket.objects.all()):
        if i % 3:
            t.assigned_to = WORKERS.pop()
            yield t

    for u in workers:

        TICKETS = Cycler(Ticket.objects.filter(assigned_to=u))
        if len(TICKETS) == 0:
            continue

        for date in (dd.demo_date(), dd.demo_date(-1), dd.demo_date(-3)):
            worked = Duration()
            ts = datetime.datetime.combine(date, datetime.time(9, 0, 0))
            for i in range(7):
                obj = Session(
                    ticket=TICKETS.pop(), session_type=TYPES.pop(), user=u)
                obj.set_datetime('start', ts)
                d = DURATIONS.pop()
                ts = DurationUnits.minutes.add_duration(ts, d)
                obj.set_datetime('end', ts)
                yield obj
                worked += d
                if worked > 8:
                    break

    ServiceReport = rt.modules.clocking.ServiceReport
    Site = rt.modules.tickets.Site
    welket = Site.objects.get(name="welket")
    yield ServiceReport(
        start_date=dd.today(-90), interesting_for=welket)
