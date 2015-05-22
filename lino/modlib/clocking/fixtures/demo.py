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
    USERS = Cycler(User.objects.all())
    TYPES = Cycler(SessionType.objects.all())
    TICKETS = Cycler(Ticket.objects.all())
    DURATIONS = Cycler([5, 12, 13, 20, 10, 20, 20, 3, 6, 17, 23])

    ts = datetime.datetime.combine(
        dd.demo_date(), datetime.time(9, 0, 0))

    for i in range(20):
        obj = Session(
            ticket=TICKETS.pop(), session_type=TYPES.pop(), user=USERS.pop())
        obj.set_datetime('start', ts)
        ts = DurationUnits.minutes.add_duration(ts, DURATIONS.pop())
        obj.set_datetime('end', ts)
        yield obj
